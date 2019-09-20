from .views import AddAnswer
from django.urls import path


urlpatterns = [

    path(r'add_answer/<int:id>', AddAnswer.as_view(), name='add_answer'),

]
