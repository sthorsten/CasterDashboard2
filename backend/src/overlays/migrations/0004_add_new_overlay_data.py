from django.db import migrations


class Migration(migrations.Migration):
    def add_data_to_leagues(apps, schema_editor):
        League = apps.get_model('main', 'League')
        CustomDesignStyle = apps.get_model('overlays', 'CustomDesignStyle')

        leagues = League.objects.all()
        for league in leagues:
            custom_design_style = CustomDesignStyle(league=league)
            custom_design_style.save()

    def add_data_to_users(apps, schema_editor):
        User = apps.get_model('auth', 'User')
        UserOverlay = apps.get_model('overlays', 'UserOverlay')

        users = User.objects.all()
        for user in users:
            user_overlay = UserOverlay(user=user)
            user_overlay.save()

    dependencies = [
        ('overlays', '0003_alter_customdesignstyle_options_and_more')
    ]

    operations = [
        migrations.RunPython(add_data_to_leagues),
        migrations.RunPython(add_data_to_users)
    ]
