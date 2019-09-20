from .views import AddComment
from django.urls import path

urlpatterns = [


    path(r'add_comment/<int:id>', AddComment.as_view(), name='add_comment'),
]
