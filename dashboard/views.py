from django.shortcuts import render
from .models import Vote, Question, Answer, Comment
from question.views import Ques
from django.views import View
from django.http import HttpResponse


class LoginHome(View):

    def get(self,request,*args,**kwargs):

        ques_list = Question.objects.filter(user_id=request.user.id)
        ans_list = Answer.objects.filter(user_id=request.user.id)
        ques_comments = dict()
        ans_comments = dict()
        for q in ques_list:
            c = q.comment.all()
            ques_comments[q] = []
            for comment in c:
                ques_comments[q].append(comment)
        for a in ans_list:
            c = a.comment.all()
            ans_comments[a] = []
            for comment in c:
                ans_comments[a].append(comment)
        return render(request, "dashboard/home.html", {'question_list': ques_comments, 'answer_list': ans_comments})

    def post(self,request,*args, **kwargs):

        return HttpResponse("Invalid Request")


class GiveVote(View):


    def get(self, request, *args, **kwargs):

        return HttpResponse("Invalid Request")


    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            if request.POST.get('type') == "question":
                ques = Question.objects.get(pk=kwargs['id'])
                print("questions")
                if 'upvote' in request.POST:

                    if ques.vote.filter(activity_type=Vote.UP_VOTE,user_id=request.user.id).count() == 0:
                        ques.vote.create(activity_type=Vote.UP_VOTE, user=request.user)
                        ques.vote.filter(activity_type=Vote.DOWN_VOTE,user=request.user).delete()
                    else:
                        ques.vote.filter(activity_type=Vote.UP_VOTE, user=request.user).delete()

                else:
                    if ques.vote.filter(activity_type=Vote.DOWN_VOTE,user_id=request.user.id).count() == 0:
                        ques.vote.create(activity_type=Vote.DOWN_VOTE, user=request.user)
                        ques.vote.filter(activity_type=Vote.UP_VOTE,user=request.user).delete()
                    else:
                        ques.vote.filter(activity_type=Vote.DOWN_VOTE, user=request.user).delete()

            elif request.POST.get('type') == "answer":
                answer = Answer.objects.get(pk=kwargs['id'])
                if 'upvote' in request.POST:
                    if answer.vote.filter(activity_type=Vote.UP_VOTE, user_id=request.user.id).count() == 0:
                        answer.vote.create(activity_type=Vote.UP_VOTE, user=request.user)
                        answer.vote.filter(activity_type=Vote.DOWN_VOTE, user=request.user).delete()
                    else:
                        answer.vote.filter(activity_type=Vote.UP_VOTE, user=request.user).delete()
                else:
                    if answer.vote.filter(activity_type=Vote.DOWN_VOTE, user_id=request.user.id).count() == 0:
                        answer.vote.create(activity_type=Vote.DOWN_VOTE, user=request.user)
                        answer.vote.filter(activity_type=Vote.UP_VOTE, user=request.user).delete()
                    else:
                        answer.vote.filter(activity_type=Vote.DOWN_VOTE, user=request.user).delete()

            else:
                comment = Comment.objects.get(pk=kwargs['id'])
                if 'upvote' in request.POST:
                    if comment.vote.filter(activity_type=Vote.UP_VOTE, user_id=request.user.id).count() == 0:
                        comment.vote.create(activity_type=Vote.UP_VOTE, user=request.user)
                        comment.vote.filter(activity_type=Vote.DOWN_VOTE, user=request.user).delete()
                    else:
                        comment.vote.filter(activity_type=Vote.UP_VOTE, user=request.user).delete()
                else:
                    if comment.vote.filter(activity_type=Vote.DOWN_VOTE, user_id=request.user.id).count() == 0:
                        comment.vote.create(activity_type=Vote.DOWN_VOTE, user=request.user)
                        comment.vote.filter(activity_type=Vote.UP_VOTE, user=request.user).delete()
                    else:
                        comment.vote.filter(activity_type=Vote.DOWN_VOTE, user=request.user).delete()

        kwargs['id'] = request.POST.get('id')
        return Ques.get(self, request, **kwargs)
