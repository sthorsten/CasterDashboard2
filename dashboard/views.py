from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import auth
from django.contrib import messages
from django.utils.translation import gettext as _

from dashboard.models import *
from overlays.models import *


def index(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/login')
    else:
        return redirect('home')


def login_view(request):
    return render(request, 'login/login.html')


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


def register(request):
    return render(request, 'login/register.html')


def register_success(requset):
    return render(requset, 'login/register-success.html')


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


def logout_view(request):
    logout(request)
    messages.success(request, _("You have been logged out! See you next time!"),
                   extra_tags=_("Logged out"))
    return redirect('/')


@login_required
def home(request):
    league_count = len(League.objects.all())
    match_count = len(Match.objects.all())
    round_count = len(Round.objects.all())

    template_data = {
        'league_count': league_count,
        'match_count': match_count,
        'round_count': round_count,
    }

    return render(request, 'index.html', template_data)


@login_required
def overlay_control_center(request):
    overlay_styles = OverlayStyle.objects.filter(user=request.user).first()
    overlay_states = OverlayState.objects.filter(user=request.user).first()
    timer_overlay_data = TimerOverlayData.objects.filter(user=request.user).first()
    # Last 10 Matches
    matches = Match.objects.filter(user=request.user).order_by("-id").all()[:10]
    match_overlay_data = MatchOverlayData.objects.filter(user=request.user).first()
    current_match = Match.objects.filter(id=match_overlay_data.current_match.id).first()

    template_data = {
        'overlay_styles': overlay_styles,
        'overlay_states': overlay_states,
        'timer_overlay_data': timer_overlay_data,
        'matches': matches,
        'match_overlay_data': match_overlay_data,
        'current_match': current_match,
    }

    return render(request, 'overlays/control-center.html', template_data)
