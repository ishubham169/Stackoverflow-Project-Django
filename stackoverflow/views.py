from django.shortcuts import redirect


def welcome(request):

    if request.user.is_authenticated:

        return redirect('dashboard_login_home')

    else:

        return redirect('dashboard_home')
