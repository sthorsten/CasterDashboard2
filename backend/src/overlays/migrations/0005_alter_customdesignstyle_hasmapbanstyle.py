# Generated by Django 4.0.3 on 2022-04-23 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overlays', '0004_add_new_overlay_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customdesignstyle',
            name='hasMapBanStyle',
            field=models.BooleanField(default=False, verbose_name='has map ban style'),
        ),
    ]
