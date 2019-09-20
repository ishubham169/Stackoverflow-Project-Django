from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey


class Vote(models.Model):

    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.activity_type


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote = GenericRelation(Vote)

    def __str__(self):
        return self.text[:10]


class Question(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.TextField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    comment = GenericRelation(Comment, related_query_name='question')
    vote = GenericRelation(Vote)

    def __str__(self):
        return self.title


class Answer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    comment = GenericRelation(Comment, related_query_name='answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = GenericRelation(Vote)

    def __str__(self):
        return self.text
