from django.contrib.auth import get_user_model
from django.db import migrations

# pylint: skip-file


class Migration(migrations.Migration):

    def create_maps(apps, schema_editor):
        """Create all necessary Rainbow Six Siege Maps"""

        Map = apps.get_model('core', 'Map')

        Map.objects.create(name='Chalet')
        Map.objects.create(name='Skyscraper')

    def update_map_pools(apps, schema_editor):
        Map = apps.get_model('core', 'Map')
        MapPool = apps.get_model('core', 'MapPool')

        # Clear all maps and re-add them
        all_map_pool = MapPool.objects.get(name="All")
        all_map_pool.maps.clear()

        all_maps = Map.objects.all()
        for all_m in all_maps:
            all_map_pool.maps.add(all_m)
        all_map_pool.save()

        # Clear competitive map pool and re-add maps
        competitive_map_pool = MapPool.objects.get(name='Competitive')
        competitive_map_pool.maps.clear()
        bank = Map.objects.get(name='Bank')
        border = Map.objects.get(name='Border')
        chalet = Map.objects.get(name='Chalet')
        clubhouse = Map.objects.get(name='Clubhouse')
        kafe = Map.objects.get(name='Kafe Dostoyevsky')
        oregon = Map.objects.get(name='Oregon')
        skyscraper = Map.objects.get(name='Skyscraper')
        themepark = Map.objects.get(name='Theme Park')
        villa = Map.objects.get(name='Villa')

        competitive_map_pool.maps.add(bank)
        competitive_map_pool.maps.add(border)
        competitive_map_pool.maps.add(chalet)
        competitive_map_pool.maps.add(clubhouse)
        competitive_map_pool.maps.add(kafe)
        competitive_map_pool.maps.add(oregon)
        competitive_map_pool.maps.add(skyscraper)
        competitive_map_pool.maps.add(themepark)
        competitive_map_pool.maps.add(villa)
        competitive_map_pool.save()

    def create_bomb_spots(apps, schema_editor):
        Map = apps.get_model('core', 'Map')
        BombSpot = apps.get_model('core', 'BombSpot')

        # Chalet
        chalet = Map.objects.get(name='Chalet')
        BombSpot.objects.create(map=chalet, floor='B',
                                name='Lockers / CCTV Room')
        BombSpot.objects.create(map=chalet, floor='B/1F',
                                name='Tellers Office / Archives')
        BombSpot.objects.create(map=chalet, floor='1F',
                                name='Open Area / Staff Room')
        BombSpot.objects.create(map=chalet, floor='2F',
                                name='CEO Office / Executive Lounge')

        # Skyscraper
        skyscraper = Map.objects.get(name='Skyscraper')
        BombSpot.objects.create(map=skyscraper, floor='1F',
                                name='Ventilation Room / Workshop')
        BombSpot.objects.create(map=skyscraper, floor='1F',
                                name='Customs Inspection / Supply Room')
        BombSpot.objects.create(map=skyscraper, floor='1F',
                                name='Bathroom / Tellers Office')
        BombSpot.objects.create(map=skyscraper, floor='2F',
                                name='Armory Lockers / Archives')

    def add_map_images(apps, schema_editor):
        Map = apps.get_model('core', 'Map')

        bank = Map.objects.get(name='Bank')
        border = Map.objects.get(name='Border')
        chalet = Map.objects.get(name='Chalet')
        clubhouse = Map.objects.get(name='Clubhouse')
        coastline = Map.objects.get(name='Coastline')
        consulate = Map.objects.get(name='Consulate')
        kafe = Map.objects.get(name='Kafe Dostoyevsky')
        oregon = Map.objects.get(name='Oregon')
        skyscraper = Map.objects.get(name='Skyscraper')
        themepark = Map.objects.get(name='Theme Park')
        villa = Map.objects.get(name='Villa')

        bank.image = 'maps/bank.webp'
        border.image = 'maps/border.webp'
        chalet.image = 'maps/chalet.webp'
        clubhouse.image = 'maps/clubhouse.webp'
        coastline.image = 'maps/coastline.webp'
        consulate.image = 'maps/consulate.webp'
        kafe.image = 'maps/kafe.webp'
        oregon.image = 'maps/oregon.webp'
        skyscraper.image = 'maps/skyscraper.webp'
        themepark.image = 'maps/themepark.webp'
        villa.image = 'maps/villa.webp'

        bank.save()
        border.save()
        chalet.save()
        clubhouse.save()
        coastline.save()
        consulate.save()
        kafe.save()
        oregon.save()
        skyscraper.save()
        themepark.save()
        villa.save()

    dependencies = [
        ('core', '0003_map_image')
    ]

    operations = [
        migrations.RunPython(create_maps),
        migrations.RunPython(update_map_pools),
        migrations.RunPython(create_bomb_spots),
        migrations.RunPython(add_map_images)
    ]
