from dashboard.models import Question, Answer, Comment
from question.views import Ques
from django.views import View
from django.http import HttpResponse
from django.core.cache import cache


class AddComment(View):

    def get(self, request, *args, **kwargs):

        return HttpResponse("Invalid Page")


    def post(self, request, *args, **kwargs):

        comment = request.POST.get('comment')

        if len(comment) == 0:
            kwargs['id'] = request.POST.get('id')
            return Ques.get(self, request, **kwargs)



        if request.POST.get('type') == "question":
            key = 'question_comment_id=' + str(kwargs['id'])
            cache_value = cache.get(key)
            if cache_value is not None:
                ques = cache_value
            else:
                ques = Question.objects.get(pk=kwargs['id'])
                cache.set(key, ques)

            Comment.objects.create(text=comment, content_object=ques, user=ques.user)


        else:
            key = 'answer_comment_id=' + str(kwargs['id'])
            cache_value = cache.get(key)
            if cache_value is not None:
                answer = cache_value
            else:
                answer = Answer.objects.get(pk=kwargs['id'])
                cache.set(key, answer)
            Comment.objects.create(text=comment, content_object=answer, user=answer.user)


        kwargs['id'] = request.POST.get('id')
        return Ques.get(self, request, **kwargs)
