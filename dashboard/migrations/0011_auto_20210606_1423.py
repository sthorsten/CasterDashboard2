# Generated by Django 3.2.4 on 2021-06-06 12:23

import dashboard.models.models
import dashboard.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20210606_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='league_logo',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.league_logo_upload_path, validators=[dashboard.validators.validate_square_logo]),
        ),
        migrations.AlterField(
            model_name='league',
            name='league_logo_small',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.league_logo_upload_path),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='dark_logo',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.sponsor_logo_upload_path),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='light_logo',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.sponsor_logo_upload_path),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='sponsor_logo',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.sponsor_logo_upload_path),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.team_logo_upload_path, validators=[dashboard.validators.validate_square_logo]),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo_small',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.team_logo_upload_path),
        ),
    ]
