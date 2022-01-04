from django.contrib.auth import get_user_model
from django.db import migrations

# pylint: skip-file

class Migration(migrations.Migration):

    def create_maps(apps, schema_editor):
        """Create all necessary Rainbow Six Siege Maps"""

        Map = apps.get_model('core', 'Map')

        Map.objects.create(name='Bank')
        Map.objects.create(name='Border')
        Map.objects.create(name='Clubhouse')
        Map.objects.create(name='Coastline')
        Map.objects.create(name='Consulate')
        Map.objects.create(name='Kafe Dostoyevsky')
        Map.objects.create(name='Oregon')
        Map.objects.create(name='Theme Park')
        Map.objects.create(name='Villa')

    def create_map_pools(apps, schema_editor):
        Map = apps.get_model('core', 'Map')
        MapPool = apps.get_model('core', 'MapPool')

        all_map_pool = MapPool.objects.create(name="All")
        all_maps = Map.objects.all()
        for all_m in all_maps:
            all_map_pool.maps.add(all_m)
        all_map_pool.save()

        competitive_map_pool = MapPool.objects.create(name='Competitive')
        competitive_maps = Map.objects.exclude(
            name__in=['Border', 'Consulate']).all()
        for comp_m in competitive_maps:
            competitive_map_pool.maps.add(comp_m)
        competitive_map_pool.save()

    def create_bomb_spots(apps, schema_editor):
        Map = apps.get_model('core', 'Map')
        BombSpot = apps.get_model('core', 'BombSpot')

        # Bank
        bank = Map.objects.get(name='Bank')
        BombSpot.objects.create(map=bank, floor='B',
                                name='Lockers / CCTV Room')
        BombSpot.objects.create(map=bank, floor='B/1F',
                                name='Tellers Office / Archives')
        BombSpot.objects.create(map=bank, floor='1F',
                                name='Open Area / Staff Room')
        BombSpot.objects.create(map=bank, floor='2F',
                                name='CEO Office / Executive Lounge')

        # Border
        border = Map.objects.get(name='Border')
        BombSpot.objects.create(map=border, floor='1F',
                                name='Ventilation Room / Workshop')
        BombSpot.objects.create(map=border, floor='1F',
                                name='Customs Inspection / Supply Room')
        BombSpot.objects.create(map=border, floor='1F',
                                name='Bathroom / Tellers Office')
        BombSpot.objects.create(map=border, floor='2F',
                                name='Armory Lockers / Archives')

        # Clubhouse
        clubhouse = Map.objects.get(name='Clubhouse')
        BombSpot.objects.create(map=clubhouse, floor='B',
                                name='Church / Arsenal Room')
        BombSpot.objects.create(
            map=clubhouse, floor='1F', name='Bar / Stage')
        BombSpot.objects.create(
            map=clubhouse, floor='2F', name='Cash / CCTV Room')
        BombSpot.objects.create(map=clubhouse, floor='2F',
                                name='Gym / Master Bedroom')

        # Coastline
        coastline = Map.objects.get(name='Coastline')
        BombSpot.objects.create(map=coastline, floor='1F',
                                name='Kitchen / Service Entrance')
        BombSpot.objects.create(map=coastline, floor='1F',
                                name='Blue Bar / Sunrise Bar')
        BombSpot.objects.create(map=coastline, floor='2F',
                                name='Hookah Lounge / Billiards Room')
        BombSpot.objects.create(map=coastline, floor='2F',
                                name='Penthouse / Theater')

        # Consulate
        consulate = Map.objects.get(name='Consulate')
        BombSpot.objects.create(map=consulate, floor='B',
                                name='Garage / Cafeteria')
        BombSpot.objects.create(map=consulate, floor='1F',
                                name='Tellers Office / Archives')
        BombSpot.objects.create(map=consulate, floor='1F',
                                name='Lobby / Press Room')
        BombSpot.objects.create(map=consulate, floor='2F',
                                name='Consulate Office / Meeting Room')

        # Kafe Dostoyevsky
        kafe = Map.objects.get(name='Kafe Dostoyevsky')
        BombSpot.objects.create(map=kafe, floor='1F',
                                name='Kitchen Service / Kitchen Cooking')
        BombSpot.objects.create(map=kafe, floor='2F',
                                name='Reading Room / Fireplace Hall')
        BombSpot.objects.create(map=kafe, floor='2F',
                                name='Fireplace Hall / Mining Room')
        BombSpot.objects.create(map=kafe, floor='3F',
                                name='Cocktail Lounge / Bar')

        # Oregon
        oregon = Map.objects.get(name='Oregon')
        BombSpot.objects.create(map=oregon, floor='B',
                                name='Laundry / Supply Room')
        BombSpot.objects.create(map=oregon, floor='1F',
                                name='Kitchen / Dining Hall')
        BombSpot.objects.create(map=oregon, floor='1F',
                                name='Meeting Hall / Kitchen')
        BombSpot.objects.create(map=oregon, floor='2F',
                                name='Kids Dorms / Dorm Main Hall')

        # Theme Park
        theme_park = Map.objects.get(name='Theme Park')
        BombSpot.objects.create(
            map=theme_park, floor='1F', name='Armory / Throne Room')
        BombSpot.objects.create(
            map=theme_park, floor='1F', name='Drugs Lab / Storage Room')
        BombSpot.objects.create(
            map=theme_park, floor='2F', name='Bunk / Day Care')
        BombSpot.objects.create(
            map=theme_park, floor='2F', name='Initiation Room / Office')

        # Villa
        villa = Map.objects.get(name='Villa')
        BombSpot.objects.create(map=villa, floor='1F',
                                name='Kitchen / Dining Room')
        BombSpot.objects.create(map=villa, floor='1F',
                                name='Living Room / Library')
        BombSpot.objects.create(map=villa, floor='2F',
                                name='Aviator Room / Games Room')
        BombSpot.objects.create(map=villa, floor='2F',
                                name='Trophy Room / Statuary Room')

    def create_operators(apps, schema_editor):
        Operator = apps.get_model('core', 'Operator')

        # Sorted by Season
        Operator.objects.create(name='_None', identifier='_none', side='ATK')
        Operator.objects.create(name='_None', identifier='_none', side='DEF')
        Operator.objects.create(name='Sledge', identifier='sledge', side='ATK')
        Operator.objects.create(
            name='Thatcher', identifier='thatcher', side='ATK')
        Operator.objects.create(name='Smoke', identifier='smoke', side='DEF')
        Operator.objects.create(name='Mute', identifier='mute', side='DEF')
        Operator.objects.create(name='Ash', identifier='ash', side='ATK')
        Operator.objects.create(
            name='Thermite', identifier='thermite', side='ATK')
        Operator.objects.create(name='Castle', identifier='castle', side='DEF')
        Operator.objects.create(name='Pulse', identifier='pulse', side='DEF')
        Operator.objects.create(name='Twitch', identifier='twitch', side='ATK')
        Operator.objects.create(
            name='Montagne', identifier='montagne', side='ATK')
        Operator.objects.create(name='Doc', identifier='doc', side='DEF')
        Operator.objects.create(name='Rook', identifier='rook', side='DEF')
        Operator.objects.create(name='Glaz', identifier='glaz', side='ATK')
        Operator.objects.create(name='Fuze', identifier='fuze', side='ATK')
        Operator.objects.create(name='Kapkan', identifier='kapkan', side='DEF')
        Operator.objects.create(
            name='Tachanka', identifier='tachanka', side='DEF')
        Operator.objects.create(name='Blitz', identifier='blitz', side='ATK')
        Operator.objects.create(name='IQ', identifier='iq', side='ATK')
        Operator.objects.create(name='Jäger', identifier='jager', side='DEF')
        Operator.objects.create(name='Bandit', identifier='bandit', side='DEF')
        Operator.objects.create(name='Buck', identifier='buck', side='ATK')
        Operator.objects.create(name='Frost', identifier='frost', side='DEF')
        Operator.objects.create(
            name='Blackbeard', identifier='blackbeard', side='ATK')
        Operator.objects.create(
            name='Valkyrie', identifier='valkyrie', side='DEF')
        Operator.objects.create(
            name='Capitão', identifier='capitao', side='ATK')
        Operator.objects.create(
            name='Caveira', identifier='caveira', side='DEF')
        Operator.objects.create(name='Hibana', identifier='hibana', side='ATK')
        Operator.objects.create(name='Echo', identifier='echo', side='DEF')
        Operator.objects.create(name='Jackal', identifier='jackal', side='ATK')
        Operator.objects.create(name='Mira', identifier='mira', side='DEF')
        Operator.objects.create(name='Ying', identifier='ying', side='ATK')
        Operator.objects.create(name='Lesion', identifier='lesion', side='DEF')
        Operator.objects.create(name='Zofia', identifier='zofia', side='ATK')
        Operator.objects.create(name='Ela', identifier='ela', side='DEF')
        Operator.objects.create(
            name='Dokkaebi', identifier='dokkaebi', side='ATK')
        Operator.objects.create(name='Vigil', identifier='vigil', side='DEF')
        Operator.objects.create(name='Lion', identifier='lion', side='ATK')
        Operator.objects.create(name='Finka', identifier='finka', side='ATK')
        Operator.objects.create(name='Alibi', identifier='alibi', side='DEF')
        Operator.objects.create(
            name='Maestro', identifier='maestro', side='DEF')
        Operator.objects.create(
            name='Maverick', identifier='maverick', side='ATK')
        Operator.objects.create(name='Clash', identifier='clash', side='DEF')
        Operator.objects.create(name='Nomad', identifier='nomad', side='ATK')
        Operator.objects.create(name='Kaid', identifier='kaid', side='DEF')
        Operator.objects.create(
            name='Gridlock', identifier='gridlock', side='ATK')
        Operator.objects.create(name='Mozzie', identifier='mozzie', side='DEF')
        Operator.objects.create(name='Nøkk', identifier='nokk', side='ATK')
        Operator.objects.create(name='Warden', identifier='warden', side='DEF')
        Operator.objects.create(name='Amaru', identifier='amaru', side='ATK')
        Operator.objects.create(name='Goyo', identifier='goyo', side='DEF')
        Operator.objects.create(name='Kali', identifier='kali', side='ATK')
        Operator.objects.create(name='Wamai', identifier='wamai', side='DEF')
        Operator.objects.create(name='Iana', identifier='iana', side='ATK')
        Operator.objects.create(name='Oryx', identifier='oryx', side='DEF')
        Operator.objects.create(name='Ace', identifier='ace', side='ATK')
        Operator.objects.create(name='Melusi', identifier='melusi', side='DEF')
        Operator.objects.create(name='Zero', identifier='zero', side='ATK')
        Operator.objects.create(name='Aruni', identifier='aruni', side='DEF')
        Operator.objects.create(name='Flores', identifier='flores', side='ATK')
        Operator.objects.create(
            name='Thunderbird', identifier='thunderbird', side='DEF')
        Operator.objects.create(name='Osa', identifier='osa', side='ATK')
        Operator.objects.create(name='Thorn', identifier='thorn', side='DEF')

    def create_default_admin_user(apps, schema_editor):
        # Create default admin user
        # Username: admin
        # Password: caster_dashboard_2

        User = get_user_model()
        admin_user = User.objects.create_user(
            "admin", None, "caster_dashboard_2")
        admin_user.is_staff = True
        admin_user.is_admin = True
        admin_user.is_superuser = True
        admin_user.save()

    dependencies = [
        ('core', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_maps),
        migrations.RunPython(create_map_pools),
        migrations.RunPython(create_bomb_spots),
        migrations.RunPython(create_operators),
        migrations.RunPython(create_default_admin_user)
    ]
