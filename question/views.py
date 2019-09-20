from dashboard.models import Question, Answer, Vote
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.core.cache import cache



class Home(View):


    def get(self, request, *args, **kwargs):

        question_list = Question.objects.all()
        response = []

        for ques in question_list:
            response.append(ques)

        return render(request, "dashboard/welcome.html", {'question_list': response})

    def post(self, request, *args, **kwargs):

        return HttpResponse("Invalid Request")


class AskQuestion(View):


    def get(self, request, *args, **kwargs):

        return render(request, 'question/ask_question.html')


    def post(self, request, *args, **kwargs):

        title = request.POST.get('title')
        text = request.POST.get('text')

        if len(title) == 0 or len(text) == 0:
            return render(request, 'question/ask_question.html')

        Question.objects.create(title=title, text=text, user=request.user)

        return Home.get(self, request)



class Ques(View):

    def get(self, request, *args, **kwargs):

        key = 'question_id=' + str(kwargs['id'])
        cache_data = cache.get(key)
        if request.user.is_authenticated == False:
            return render(request, "question/question.html", {'Object': cache_data, 'id': kwargs['id']})
        if cache_data is not None:
            value = cache.get(key)
            quest = value['question']
        else:
            quest = Question.objects.get(id=kwargs['id'])
        response = dict()
        response['question'] = quest
        response['upvote'] = quest.vote.filter(activity_type=Vote.UP_VOTE).count()
        response['downvote'] = quest.vote.filter(activity_type=Vote.DOWN_VOTE).count()
        response['vote'] = response['upvote'] - response['downvote']
        response['comments'] = []
        response['answers'] = []

        comments = []
        for comment in quest.comment.all():
            d = dict()
            d['comment'] = comment
            d['upvote'] = comment.vote.filter(activity_type=Vote.UP_VOTE).count()
            d['downvote'] = comment.vote.filter(activity_type=Vote.DOWN_VOTE).count()
            d['vote'] = d['upvote'] - d['downvote']
            comments.append(d)

        response['comments'] = comments

        ans_list = Answer.objects.filter(question_id=kwargs['id'])
        answer = []

        for ans in ans_list:
            d = dict()
            d['answer'] = ans
            d['upvote'] = ans.vote.filter(activity_type=Vote.UP_VOTE).count()
            d['downvote'] = ans.vote.filter(activity_type=Vote.DOWN_VOTE).count()
            d['vote'] = d['upvote'] - d['downvote']
            d['comments'] = []
            comments = []
            for comment in ans.comment.all():
                c = dict()
                c['comment'] = comment
                c['upvote'] = comment.vote.filter(activity_type=Vote.UP_VOTE).count()
                c['downvote'] = comment.vote.filter(activity_type=Vote.DOWN_VOTE).count()
                c['vote'] = c['upvote'] - c['downvote']
                comments.append(c)
            d['comments'].append(comments)
            answer.append(d)
        response['answers'] = answer
        cache.set(key,response)
        return render(request, "question/question.html", {'Object': response, 'id': kwargs['id']})

    def post(self, request, *args, **kwargs):

        return HttpResponse("Invalid Response")
