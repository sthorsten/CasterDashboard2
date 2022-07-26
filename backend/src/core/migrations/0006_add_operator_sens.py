from django.db import migrations

# pylint: skip-file


class Migration(migrations.Migration):
    def add_operator_sens(apps, schema_editor):
        Operator = apps.get_model('core', 'Operator')
        Operator.objects.create(name='Sens', identifier='sens', side='ATK')

    dependencies = [
        ('core', '0005_add_operator_azami')
    ]

    operations = [
        migrations.RunPython(add_operator_sens)
    ]
