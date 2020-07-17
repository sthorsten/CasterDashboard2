import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from dashboard.models import *

logger = logging.getLogger(__name__)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile = Profile.objects.filter(user=user).first()
            if not profile.confirmed:
                logger.info("[User: %s] Login failed: Account not confirmed" % user)
                messages.error(request, _("Your account must be confirmed by an admin before you can login"),
                               extra_tags=_("Login failed"))
                return redirect('/login')

            login(request, user)
            logger.info("[User: %s] Login successful." % user)
            messages.success(request, _("You have been logged in successfully"), extra_tags=_("Welcome %s!" % user))
            return redirect('/dashboard/home')
        else:
            logger.info("[User: %s] Login faild: Invalid credentials" % username)
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
            logging.info("[User: %s] New registration" % user)
            return redirect('/register/success')
        else:
            logging.error("[User: %s] Registration failed!" % username)
            messages.error(request, _("Your account could not be created! Please try again or contact an admin!"),
                           extra_tags=_("Registration failed"))
            return redirect('/login')

    return render(request, 'login/register.html')


'''
    New Match form
'''


@login_required
def new_match_form(request):
    if not request.method == 'POST':
        return redirect('/dashboard/matches/create')

    data = request.POST

    # Check data
    if not data['new-match-league'] or not data['new-match-season'] or not data['new-match-bestof'] or not data[
        'new-match-title'] or not data['new-match-team-blue'] or not data['new-match-team-orange']:
        messages.error(request, _("The match could not be created"), extra_tags=_("Invalid Match Data"))
        return redirect('/dashboard/matches/create')

    season = Season.objects.filter(id=data['new-match-season']).first()
    league = League.objects.filter(id=data['new-match-league']).first()
    team_blue = Team.objects.filter(id=data['new-match-team-blue']).first()
    team_orange = Team.objects.filter(id=data['new-match-team-orange']).first()

    match = Match(season=season, league=league, title=data['new-match-title'],
                  subtitle=data['new-match-subtitle'], state="created", best_of=data['new-match-bestof'],
                  team_blue=team_blue, team_orange=team_orange)
    try:
        match.save()
        match.user.add(request.user)
        match.save()
    except DatabaseError:
        messages.error(request, _("The match could not be created"), extra_tags=_("Database Error"))
        return redirect('/dashboard/matches/create')

    messages.success(request, _("The match has been created successfully"), extra_tags=_(_("Match created")))
    return redirect('/dashboard/matches/create')
