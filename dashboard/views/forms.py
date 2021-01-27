import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import gettext as _
from pip._vendor import requests

import caster_dashboard_2
import caster_dashboard_2.settings as django_settings

from dashboard.models.models import *

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
            logger.info("[User: %s] Login successful" % user)
            messages.success(request, _("You have been logged in successfully"), extra_tags=_("Welcome %s!" % user))

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)

            return redirect('/dashboard/home')
        else:
            logger.info("[User: %s] Login failed: Invalid credentials" % username)
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

            # Email confirmation
            profile = Profile.objects.get(user=user)
            user_token = profile.registration_token
            email_text = get_template("email/register_email.txt")
            email_html = get_template("email/register_email.html")
            email_context = {'username': user.username, 'user_id': user.id, 'token': user_token}
            from_email = caster_dashboard_2.settings.local_settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject="[Caster Dashboard] Account Registration",
                from_email=from_email,
                recipient_list=[user.email],
                message=email_text.render(email_context),
                html_message=email_html.render(email_context),
            )

            return redirect('/register/success')
        else:
            logging.error("[User: %s] Registration failed!" % username)
            messages.error(request, _("Your account could not be created! Please try again or contact an admin!"),
                           extra_tags=_("Registration failed"))
            return redirect('/login')

    return render(request, 'login/register.html')


'''
    Data Forms
'''


@login_required
def new_team_form(request):
    if not request.method == 'POST':
        return redirect('/dashboard/data/teams')

    logger.info("[User: %s] Creating a new team..." % request.user)

    data = request.POST

    # Validate / Format
    if not len(data['team_name']) > 0:
        logger.warning("[User: %s] Team creation failed: No team name" % request.user)
        messages.error(request, _("No team name"), extra_tags=_("Team creation failed"))
        return redirect('/dashboard/data/teams')

    # Handle files
    if not request.FILES:
        if not len(data['logo_url']) > 0:
            if not data.get('no_logo'):
                logger.warning(
                    "[User: %s] [Team: %s] Team creation failed: No logo option" % (request.user, data['team_name']))
                messages.error(request, _("Please add a logo or select 'Team has no logo'"),
                               extra_tags=_("Team creation failed"))
                return redirect('/dashboard/data/teams')

            else:
                try:
                    logger.info(
                        "[User: %s] [Team %s] Creating team without logo..." % (request.user, data['team_name']))
                    new_team = Team(name=data['team_name'], has_logo=False)
                    new_team.save()
                    logger.info(
                        "[User: %s] [Team: %s] ...Team created successfully" % (request.user, data['team_name']))
                    messages.success(request, _("The team has been added successfully"), extra_tags=_("Team created"))

                except DatabaseError:
                    logger.error("[User: %s] [Team: %s] Team creation failed: Could not create database entry!" % (
                        request.user, data['team_name']))
                    messages.error(request, _("Database error (please report this!)'"),
                                   extra_tags=_("Team creation failed"))
                finally:
                    return redirect('/dashboard/data/teams')

        else:
            try:
                logger.info(
                    "[User: %s] [Team %s] Creating team with logo download..." % (request.user, data['team_name']))
                new_team = Team(name=data['team_name'], has_logo=True)
                new_team.save()
                new_team.team_logo = 'teams/' + str(new_team.id) + ".png"
                new_team.save()

            except DatabaseError:
                logger.error("[User: %s] [Team: %s] Team creation failed: Could not create database entry!" % (
                    request.user, data['team_name']))
                messages.error(request, _("Database error (please report this!)'"),
                               extra_tags=_("Team creation failed"))
                return redirect('/dashboard/data/teams')

            try:
                # Download and save file
                url = data['logo_url']
                r = requests.get(url, allow_redirects=True)
                save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(new_team.id) + '.png')
                open(save_path, 'wb').write(r.content)
                messages.success(request, _("The team has been added successfully"), extra_tags=_("Team created"))
                logger.info("[User: %s] [Team: %s] ...Team created successfully" % (request.user, data['team_name']))

            except requests.exceptions.RequestException:
                logger.error("[User: %s] [Team: %s] Team creation failed: Logo download failed" % (
                    request.user, data['team_name']))
                new_team.delete()
                messages.error(request, _("Team Logo could not be downloaded. Please upload it manually!"),
                               extra_tags=_("Team creation failed"))
            except OSError:
                logger.error("[User: %s] [Team: %s] Team creation failed: Logo save to disk failed" % (
                    request.user, data['team_name']))
                new_team.delete()
                messages.error(request, _("Team Logo could not be downloaded. Please upload it manually!"),
                               extra_tags=_("Team creation failed"))
            finally:
                return redirect('/dashboard/data/teams')

    else:
        try:
            new_team = Team(name=data['team_name'], has_logo=True)
            new_team.save()
            new_team.team_logo = 'teams/' + str(new_team.id) + ".png"
            new_team.save()

        except DatabaseError:
            logger.error("[User: %s] [Team: %s] Team creation failed: Could not create database entry!" % (
                request.user, data['team_name']))
            messages.error(request, _("Database error (please report this!)'"),
                           extra_tags=_("Team creation failed"))
            return redirect('/dashboard/data/teams')

        try:
            save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(new_team.id) + '.png')
            open(save_path, 'wb').write(request.FILES['logo_file'].read())
            messages.success(request, _("The team has been added successfully"), extra_tags=_("Team created"))
            logger.info("[User: %s] [Team: %s] ...Team created successfully" % (request.user, data['team_name']))

        except OSError:
            logger.error("[User: %s] [Team: %s] Team creation failed: Logo save to disk failed" % (
                request.user, data['team_name']))
            new_team.delete()
            messages.error(request, _("Team Logo could not be saved. Please try again!"),
                           extra_tags=_("Team creation failed"))
        finally:
            return redirect('/dashboard/data/teams')


@login_required
def edit_team_form(request):
    if not request.method == 'POST':
        return redirect('/dashboard/data/teams')

    logger.info("[User: %s] Editing a team..." % request.user)

    data = request.POST

    # Validate / Format
    if not data['team_id']:
        logger.warning("[User: %s] Team edit failed: No team id" % request.user)
        messages.error(request, _("No team id"), extra_tags=_("Team edit failed"))
        return redirect('/dashboard/data/teams')

    try:
        team_id = int(data['team_id'])
    except ValueError:
        logger.warning("[User: %s] Team edit failed: Invalid team id" % request.user)
        messages.error(request, _("Invalid team id"), extra_tags=_("Team edit failed"))
        return redirect('/dashboard/data/teams')

    team = Team.objects.filter(id=team_id).first()

    # Handle files
    if not request.FILES:
        if not len(data['logo_url']) > 0:
            if not data.get('no_logo'):
                logger.warning(
                    "[User: %s] [Team: %s] Team edit failed: No logo option" % (request.user, team))
                messages.error(request, _("Please add a logo or select 'Team has no logo'"),
                               extra_tags=_("Team edit failed"))
                return redirect('/dashboard/data/teams')

            else:
                try:
                    logger.info(
                        "[User: %s] [Team %s] Removing team logo..." % (request.user, team))
                    team.has_logo = False
                    team.team_logo = None
                    team.save()
                    messages.success(request, _("The team has been edited successfully"), extra_tags=_("Team edited"))

                except DatabaseError:
                    logger.error("[User: %s] [Team: %s] Team edit failed: Database save failure!" % (
                        request.user, team))
                    messages.error(request, _("Database error (please report this!)'"),
                                   extra_tags=_("Team edit failed"))
                finally:
                    logger.info(
                        "[User: %s] [Team: %s] ...Team edited successfully" % (request.user, team))
                    return redirect('/dashboard/data/teams')

        else:
            try:
                # Download and save file
                url = data['logo_url']
                r = requests.get(url, allow_redirects=True)
                save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(team.id) + '.png')
                open(save_path, 'wb').write(r.content)

            except requests.exceptions.RequestException:
                logger.error("[User: %s] [Team: %s] Team edit failed: Logo download failed" % (
                    request.user, team))
                messages.error(request, _("Team Logo could not be downloaded. Please upload it manually!"),
                               extra_tags=_("Team edit failed"))
            except OSError:
                logger.error("[User: %s] [Team: %s] Team edit failed: Logo save to disk failed" % (
                    request.user, team))
                messages.error(request, _("Team Logo could not be downloaded. Please upload it manually!"),
                               extra_tags=_("Team edit failed"))

            if not team.has_logo:
                try:
                    team.has_logo = True
                    team.team_logo = 'teams/' + str(team.id) + ".png"
                    team.save()
                    messages.success(request, _("The team has been edited successfully"), extra_tags=_("Team edited"))
                    logger.info("[User: %s] [Team: %s] ...Team edited successfully" % (request.user, team))

                except DatabaseError:
                    logger.error("[User: %s] [Team: %s] Team edit failed: Database save failed" % (
                        request.user, team))
                    messages.error(request, _("Database error (please report this!)'"),
                                   extra_tags=_("Team creation failed"))
                finally:
                    return redirect('/dashboard/data/teams')

    else:
        try:
            save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(team.id) + '.png')
            open(save_path, 'wb').write(request.FILES['logo_file'].read())

        except OSError:
            logger.error("[User: %s] [Team: %s] Team edit failed: Logo save to disk failed" % (
                request.user, team))
            messages.error(request, _("Team Logo could not be saved. Please try again!"),
                           extra_tags=_("Team edit failed"))

        if not team.has_logo:
            try:
                team.has_logo = True
                team.team_logo = 'teams/' + str(team.id) + ".png"
                team.save()
                messages.success(request, _("The team has been edited successfully"), extra_tags=_("Team edited"))
                logger.info("[User: %s] [Team: %s] ...Team edited successfully" % (request.user, team))

            except DatabaseError:
                logger.error("[User: %s] [Team: %s] Team edit failed: Database save failed" % (
                    request.user, team))
                messages.error(request, _("Database error (please report this!)'"),
                               extra_tags=_("Team creation failed"))
            finally:
                return redirect('/dashboard/data/teams')


'''
    Match Forms
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

    if data.get('new-match-dummy'):
        match_state = MatchState.objects.get(state="Dummy")
    else:
        match_state = MatchState.objects.filter(state="Created").first()

    match = Match(season=season, league=league, title=data['new-match-title'],
                  subtitle=data['new-match-subtitle'], state=match_state, best_of=data['new-match-bestof'],
                  team_blue=team_blue, team_orange=team_orange)

    try:
        match.save()
        match.user.add(request.user)
        for s_id in request.POST.getlist('new-match-sponsors'):
            sponsor = Sponsor.objects.get(id=s_id)
            match.sponsors.add(sponsor)

        match.save()
    except DatabaseError:
        messages.error(request, _("The match could not be created"), extra_tags=_("Database Error"))
        return redirect('/dashboard/matches/create')

    messages.success(request, _("The match has been created successfully"), extra_tags=_(_("Match created")))
    return redirect('/dashboard/matches/%s' % match.id)
