# Generated by Django 3.1.3 on 2021-01-27 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_set_permission_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(1, 'Information'), (2, 'Success'), (3, 'Warning'), (4, 'Danger')], default=1)),
                ('show', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('valid_until', models.DateTimeField()),
            ],
        ),
    ]
