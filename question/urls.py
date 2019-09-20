from .views import AskQuestion, Ques, Home
from django.urls import path
from django.conf.urls import url

urlpatterns = [

    path(r'ask_question>', AskQuestion.as_view(), name ='ask_question'),
    path(r'questions/<int:id>', Ques.as_view(), name='questions'),
    url(r'^$', Home.as_view(), name='dashboard_home'),
]