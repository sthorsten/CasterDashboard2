# Generated by Django 3.0.8 on 2020-07-11 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0016_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(default='user', max_length=255)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.League')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]