from django.db import migrations

# pylint: skip-file


class Migration(migrations.Migration):
    def add_operator_azami(apps, schema_editor):
        Operator = apps.get_model('core', 'Operator')
        Operator.objects.create(name='Azami', identifier='azami', side='DEF')

    dependencies = [
        ('core', '0004_map_img_and_pool')
    ]

    operations = [
        migrations.RunPython(add_operator_azami)
    ]
