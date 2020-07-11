from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from dashboard.models import *


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile = Profile.objects.filter(user=user).first()
            if not profile.confirmed:
                messages.error(request, _("Your account must be confirmed by an admin before you can login"),
                               extra_tags=_("Login failed"))
                return redirect('/login')

            login(request, user)
            messages.success(request, _("You have been logged in successfully"), extra_tags=_("Welcome %s!" % user))
            return redirect('/dashboard/home')
        else:
            messages.error(request, _("Username or password incorrect!"), extra_tags=_("Login failed"))
            return redirect('/login')

    return render(request, 'login/login.html')


def register_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)

        if user is not None:
            return redirect('/register/success')
        else:
            messages.error(request, _("Your account could not be created! Please try again or contact an admin!"),
                           extra_tags=_("Registration failed"))
            return redirect('/login')

    return render(request, 'login/register.html')
