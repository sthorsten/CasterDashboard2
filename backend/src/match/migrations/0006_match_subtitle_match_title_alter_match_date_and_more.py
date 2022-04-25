# Generated by Django 4.0.3 on 2022-04-23 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_alter_match_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='subTitle',
            field=models.CharField(blank=True, help_text='Subtitle (line 2) shown in various overlays.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='title',
            field=models.CharField(blank=True, help_text='Match title shown in various overlays.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 23, 18, 0)),
        ),
        migrations.AlterField(
            model_name='match',
            name='name',
            field=models.CharField(blank=True, help_text="Internal name. You can leave this field blank. The match name will then be set automatically, e.g. 'Team A vs. Team B'", max_length=255, null=True),
        ),
    ]