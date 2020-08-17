# Generated by Django 3.0.8 on 2020-07-27 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_round_of_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapPlayOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
            ],
        ),
    ]