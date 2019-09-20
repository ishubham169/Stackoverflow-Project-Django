from dashboard.models import Answer
from question.views import Ques
from django.views import View
from django.http import HttpResponse


class AddAnswer(View):

    def get(self, request, *args, **kwargs):

        return HttpResponse("Invalid Page")

    def post(self, request, *args, **kwargs):

        answer = request.POST.get('answer')
        if len(answer) == 0:
            return Ques.get(self, request, **kwargs)

        Answer.objects.create(text=answer, question_id=kwargs['id'], user=request.user)

        return Ques.get(self, request, **kwargs)
