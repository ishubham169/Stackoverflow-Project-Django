from .views import LoginHome, GiveVote
from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [

    url(r'^login$', LoginView.as_view(template_name="dashboard/login_form.html"), name='dashboard_login'),
    url(r'^logout$', LogoutView.as_view(), name='dashboard_logout'),
    url(r'^home$', LoginHome.as_view(), name='dashboard_login_home'),
    path(r'add_vote/<int:id>', GiveVote.as_view(), name='add_vote'),

]
