from django.db import migrations


class Migration(migrations.Migration):

    def update_map_pool(apps, schema_editor):
        Map = apps.get_model('dashboard', 'Map')
        MapPool = apps.get_model('dashboard', 'MapPool')
        BombSpot = apps.get_model('dashboard', 'BombSpot')

        # Add chalet
        chalet = Map.objects.create(name="Chalet")

        all_map_pool = MapPool.objects.get(name="All")
        comp_map_pool = MapPool.objects.get(name="Competitive")

        all_map_pool.maps.add(chalet)

        # Remove Theme Park from Competitive
        theme_park = Map.objects.get(name="Theme Park")
        comp_map_pool.maps.remove(theme_park)
        comp_map_pool.maps.add(chalet)

        all_map_pool.save()
        comp_map_pool.save()

        # Add bomb spots for chalet
        BombSpot.objects.create(map=chalet, floor='B', name='Wine Cellar / Snowmobile Garage')
        BombSpot.objects.create(map=chalet, floor='1F', name='Kitchen / Dining Room')
        BombSpot.objects.create(map=chalet, floor='1F', name='Bar / Gaming Room')
        BombSpot.objects.create(map=chalet, floor='2F', name='Office / Master Bedroom')


    dependencies = [
        ('dashboard', '0008_auto_20210401_1156')
    ]

    operations = [
        migrations.RunPython(update_map_pool)
    ]
