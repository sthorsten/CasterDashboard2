# Generated by Django 3.0.8 on 2020-09-17 08:18

import dashboard.models
import dashboard.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0049_auto_20200902_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='dark_logo',
        ),
        migrations.RemoveField(
            model_name='league',
            name='light_logo',
        ),
        migrations.AddField(
            model_name='league',
            name='league_logo_small',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.league_logo_path),
        ),
        migrations.AlterField(
            model_name='league',
            name='league_logo',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.league_logo_path, validators=[dashboard.validators.validate_square_logo]),
        ),
    ]
