from django.db import migrations


class Migration(migrations.Migration):

    def create_user_groups(apps, schema_editor):
        Group = apps.get_model('auth', 'Group')
        Permission = apps.get_model('auth', 'Permission')

        # Create groups
        user = Group(name="User")
        user.save()

        # Add permissions to groups
        bombspot_view = Permission.objects.get(codename='view_bombspot')
        leaguegroup_view = Permission.objects.get(codename='view_leaguegroup')
        map_view = Permission.objects.get(codename='view_map')
        mappool_view = Permission.objects.get(codename='view_mappool')
        league_view = Permission.objects.get(codename='view_league')
        season_view = Permission.objects.get(codename='view_season')
        sponsor_view = Permission.objects.get(codename='view_sponsor')
        operator_view = Permission.objects.get(codename='view_operator')

        match_view = Permission.objects.get(codename='view_match')
        match_add = Permission.objects.get(codename='add_match')
        match_change = Permission.objects.get(codename='change_match')
        match_delete = Permission.objects.get(codename='delete_match')

        matchmap_view = Permission.objects.get(codename='view_matchmap')
        matchmap_add = Permission.objects.get(codename='add_matchmap')
        matchmap_change = Permission.objects.get(codename='change_matchmap')
        matchmap_delete = Permission.objects.get(codename='delete_matchmap')

        opbans_view = Permission.objects.get(codename='view_operatorbans')
        opbans_add = Permission.objects.get(codename='add_operatorbans')
        opbans_change = Permission.objects.get(codename='change_operatorbans')
        opbans_delete = Permission.objects.get(codename='delete_operatorbans')

        round_view = Permission.objects.get(codename='view_round')
        round_add = Permission.objects.get(codename='add_round')
        round_change = Permission.objects.get(codename='change_round')
        round_delete = Permission.objects.get(codename='delete_round')

        team_view = Permission.objects.get(codename='view_team')
        team_add = Permission.objects.get(codename='add_team')
        team_change = Permission.objects.get(codename='change_team')

        matchoverlaydata_view = Permission.objects.get(codename='view_matchoverlaydata')
        matchoverlaydata_change = Permission.objects.get(codename='change_matchoverlaydata')

        polloverlaydata_view = Permission.objects.get(codename='view_polloverlaydata')
        polloverlaydata_change = Permission.objects.get(codename='change_polloverlaydata')

        socialoverlaydata_view = Permission.objects.get(codename='view_socialoverlaydata')
        socialoverlaydata_change = Permission.objects.get(codename='change_socialoverlaydata')

        tickeroverlaydata_view = Permission.objects.get(codename='view_tickeroverlaydata')
        tickeroverlaydata_change = Permission.objects.get(codename='change_tickeroverlaydata')

        timeroverlaydata_view = Permission.objects.get(codename='view_timeroverlaydata')
        timeroverlaydata_change = Permission.objects.get(codename='change_timeroverlaydata')

        overlaystate_view = Permission.objects.get(codename='view_overlaystate')
        overlaystate_change = Permission.objects.get(codename='change_overlaystate')

        overlaystyle_view = Permission.objects.get(codename='view_overlaystyle')
        overlaystyle_change = Permission.objects.get(codename='change_overlaystyle')

        user.permissions.add(bombspot_view, leaguegroup_view, map_view, mappool_view, league_view, season_view,
                             sponsor_view, operator_view, match_view, match_add, match_change, match_delete,
                             matchmap_view, matchmap_add, matchmap_change, matchmap_delete, opbans_view, opbans_add,
                             opbans_change, opbans_delete, round_view, round_add, round_change, round_delete, team_view,
                             team_add, team_change, matchoverlaydata_view, matchoverlaydata_change,
                             polloverlaydata_view, polloverlaydata_change, socialoverlaydata_view,
                             socialoverlaydata_change, tickeroverlaydata_view, tickeroverlaydata_change,
                             timeroverlaydata_view, timeroverlaydata_change, overlaystate_view, overlaystate_change,
                             overlaystyle_view, overlaystyle_change)

    dependencies = [
        ('dashboard', '0001_initial'),
        ('overlays', '0001_initial'),
        ('dashboard', '0002_create_default_data')
    ]

    operations = [
        migrations.RunPython(create_user_groups),
    ]
