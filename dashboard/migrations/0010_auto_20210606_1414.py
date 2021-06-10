# Generated by Django 3.2.4 on 2021-06-06 12:14

import dashboard.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_competitive_map_pool_update_Y6S1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='league_logo',
            field=models.ImageField(blank=True, null=True, upload_to='leagues/5f2768a8110a48a684beaa7cbb3d0e64_temp.png', validators=[dashboard.validators.validate_square_logo]),
        ),
        migrations.AlterField(
            model_name='league',
            name='league_logo_small',
            field=models.ImageField(blank=True, null=True, upload_to='leagues/bbbe9d98cff4476c8744bb3c554e29de_temp.png'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='dark_logo',
            field=models.ImageField(blank=True, null=True, upload_to='sponsors/e8894f4dd8a2401b960783bf0ade5172_temp.png'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='light_logo',
            field=models.ImageField(blank=True, null=True, upload_to='sponsors/09ba6d5396884a1386386501fa087b53_temp.png'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='sponsor_logo',
            field=models.ImageField(blank=True, null=True, upload_to='sponsors/70839eac9b70407b85313008854613af_temp.png'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(blank=True, null=True, upload_to='teams/4d9d69d989a04122942a278a4bfdd811_temp.png', validators=[dashboard.validators.validate_square_logo]),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo_small',
            field=models.ImageField(blank=True, null=True, upload_to='teams/3eac11ee0770439aade937d5c14cf74f_temp.png'),
        ),
    ]
