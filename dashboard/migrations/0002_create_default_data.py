from django.contrib.auth import get_user_model
from django.db import migrations

class Migration(migrations.Migration):

    def create_maps(apps, schema_editor):
        # Create all necessary Rainbow Six Siege Maps

        Map = apps.get_model('dashboard', 'Map')

        Map.objects.create(name="Bank")
        Map.objects.create(name="Border")
        Map.objects.create(name="Clubhouse")
        Map.objects.create(name="Coastline")
        Map.objects.create(name="Consulate")
        Map.objects.create(name="Kafe Dostoyevsky")
        Map.objects.create(name="Oregon")
        Map.objects.create(name="Theme Park")
        Map.objects.create(name="Villa")

    def create_map_pools(apps, schema_editor):
        Map = apps.get_model('dashboard', 'Map')
        MapPool = apps.get_model('dashboard', 'MapPool')

        all_map_pool = MapPool.objects.create(name="All")
        all_maps = Map.objects.all()
        for all_m in all_maps:
            all_map_pool.maps.add(all_m)
        all_map_pool.save()

        competitive_map_pool = MapPool.objects.create(name="Competitive")
        competitive_maps = Map.objects.exclude(name__in=["Bank", "Border"]).all()
        for comp_m in competitive_maps:
            competitive_map_pool.maps.add(comp_m)
        competitive_map_pool.save()

    def create_bomb_spots(apps, schema_editor):
        Map = apps.get_model('dashboard', 'Map')
        BombSpot = apps.get_model('dashboard', 'BombSpot')

        # Bank
        bank = Map.objects.get(name="Bank")
        BombSpot.objects.create(map=bank, floor='B', name='Lockers / CCTV Room')
        BombSpot.objects.create(map=bank, floor='1F', name='Tellers Office / Archives')
        BombSpot.objects.create(map=bank, floor='1F', name='Open Area / Staff Room')
        BombSpot.objects.create(map=bank, floor='2F', name='CEO Office / Executive Lounge')

        # Border
        border = Map.objects.get(name="Border")
        BombSpot.objects.create(map=border, floor='1F', name='Ventilation Room / Workshop')
        BombSpot.objects.create(map=border, floor='1F', name='Customs Inspection / Supply Room')
        BombSpot.objects.create(map=border, floor='1F', name='Bathroom / Tellers Office')
        BombSpot.objects.create(map=border, floor='2F', name='Armory Lockers / Archives')

        # Clubhouse
        clubhouse = Map.objects.get(name="Clubhouse")
        BombSpot.objects.create(map=clubhouse, floor='B', name='Church / Arsenal Room')
        BombSpot.objects.create(map=clubhouse, floor='1F', name='Bar / Stock Room')
        BombSpot.objects.create(map=clubhouse, floor='2F', name='Cash / CCTV Room')
        BombSpot.objects.create(map=clubhouse, floor='2F', name='Gym / Master Bedroom')

        # Coastline
        coastline = Map.objects.get(name="Coastline")
        BombSpot.objects.create(map=coastline, floor='1F', name='Kitchen / Service Entrance')
        BombSpot.objects.create(map=coastline, floor='1F', name='Blue Bar / Sunrise Bar')
        BombSpot.objects.create(map=coastline, floor='2F', name='Hookah Lounge / Billiards Room')
        BombSpot.objects.create(map=coastline, floor='2F', name='Penthouse / Theater')

        # Consulate
        consulate = Map.objects.get(name="Consulate")
        BombSpot.objects.create(map=consulate, floor='B', name='Garage / Cafeteria')
        BombSpot.objects.create(map=consulate, floor='1F', name='Tellers Office / Archives')
        BombSpot.objects.create(map=consulate, floor='1F', name='Lobby / Press Room')
        BombSpot.objects.create(map=consulate, floor='2F', name='Consulate Office / Meeting Room')

        # Kafe Dostoyevsky
        kafe = Map.objects.get(name="Kafe Dostoyevsky")
        BombSpot.objects.create(map=kafe, floor='1F', name='Kitchen Service / Kitchen Cooking')
        BombSpot.objects.create(map=kafe, floor='2F', name='Reading Room / Fireplace Hall')
        BombSpot.objects.create(map=kafe, floor='2F', name='Fireplace Hall / Mining Room')
        BombSpot.objects.create(map=kafe, floor='3F', name='Cocktail Lounge / Bar')

        # Oregon
        oregon = Map.objects.get(name="Oregon")
        BombSpot.objects.create(map=oregon, floor='B', name='Laundry / Supply Room')
        BombSpot.objects.create(map=oregon, floor='1F', name='Kitchen / Dining Hall')
        BombSpot.objects.create(map=oregon, floor='1F', name='Meeting Hall / Kitchen')
        BombSpot.objects.create(map=oregon, floor='2F', name='Kids Dorms / Dorm Main Hall')

        # Theme Park
        theme_park = Map.objects.get(name="Theme Park")
        BombSpot.objects.create(map=theme_park, floor='1F', name='Armory / Throne Room')
        BombSpot.objects.create(map=theme_park, floor='1F', name='Drugs Lab / Storage Room')
        BombSpot.objects.create(map=theme_park, floor='2F', name='Bunk / Day Care')
        BombSpot.objects.create(map=theme_park, floor='2F', name='Initiation Room / Office')

        # Villa
        villa = Map.objects.get(name="Villa")
        BombSpot.objects.create(map=villa, floor='1F', name='Kitchen / Dining Room')
        BombSpot.objects.create(map=villa, floor='1F', name='Living Room / Library')
        BombSpot.objects.create(map=villa, floor='2F', name='Aviator Room / Games Room')
        BombSpot.objects.create(map=villa, floor='2F', name='Trophy Room / Statuary Room')

    def create_operators(apps, schema_editor):
        Operator = apps.get_model('dashboard', 'Operator')

        # Sorted by Season
        Operator.objects.create(name='_None', side='ATK')
        Operator.objects.create(name='_None', side='DEF')
        Operator.objects.create(name='Sledge', side='ATK')
        Operator.objects.create(name='Thatcher', side='ATK')
        Operator.objects.create(name='Smoke', side='DEF')
        Operator.objects.create(name='Mute', side='DEF')
        Operator.objects.create(name='Ash', side='ATK')
        Operator.objects.create(name='Thermite', side='ATK')
        Operator.objects.create(name='Castle', side='DEF')
        Operator.objects.create(name='Pulse', side='DEF')
        Operator.objects.create(name='Twitch', side='ATK')
        Operator.objects.create(name='Montagne', side='ATK')
        Operator.objects.create(name='Doc', side='DEF')
        Operator.objects.create(name='Rook', side='DEF')
        Operator.objects.create(name='Glaz', side='ATK')
        Operator.objects.create(name='Fuze', side='ATK')
        Operator.objects.create(name='Kapkan', side='DEF')
        Operator.objects.create(name='Tachanka', side='DEF')
        Operator.objects.create(name='Blitz', side='ATK')
        Operator.objects.create(name='IQ', side='ATK')
        Operator.objects.create(name='Jager', side='DEF')
        Operator.objects.create(name='Bandit', side='DEF')
        Operator.objects.create(name='Buck', side='ATK')
        Operator.objects.create(name='Frost', side='DEF')
        Operator.objects.create(name='Blackbeard', side='ATK')
        Operator.objects.create(name='Valkyrie', side='DEF')
        Operator.objects.create(name='Capitao', side='ATK')
        Operator.objects.create(name='Caveira', side='DEF')
        Operator.objects.create(name='Hibana', side='ATK')
        Operator.objects.create(name='Echo', side='DEF')
        Operator.objects.create(name='Jackal', side='ATK')
        Operator.objects.create(name='Mira', side='DEF')
        Operator.objects.create(name='Ying', side='ATK')
        Operator.objects.create(name='Lesion', side='DEF')
        Operator.objects.create(name='Zofia', side='ATK')
        Operator.objects.create(name='Ela', side='DEF')
        Operator.objects.create(name='Dokkaebi', side='ATK')
        Operator.objects.create(name='Vigil', side='DEF')
        Operator.objects.create(name='Lion', side='ATK')
        Operator.objects.create(name='Finka', side='ATK')
        Operator.objects.create(name='Alibi', side='DEF')
        Operator.objects.create(name='Maestro', side='DEF')
        Operator.objects.create(name='Maverick', side='ATK')
        Operator.objects.create(name='Clash', side='DEF')
        Operator.objects.create(name='Nomad', side='ATK')
        Operator.objects.create(name='Kaid', side='DEF')
        Operator.objects.create(name='Gridlock', side='ATK')
        Operator.objects.create(name='Mozzie', side='DEF')
        Operator.objects.create(name='Nokk', side='ATK')
        Operator.objects.create(name='Warden', side='DEF')
        Operator.objects.create(name='Amaru', side='ATK')
        Operator.objects.create(name='Goyo', side='DEF')
        Operator.objects.create(name='Kali', side='ATK')
        Operator.objects.create(name='Wamai', side='DEF')
        Operator.objects.create(name='Iana', side='ATK')
        Operator.objects.create(name='Oryx', side='DEF')
        Operator.objects.create(name='Ace', side='ATK')
        Operator.objects.create(name='Melusi', side='DEF')
        Operator.objects.create(name='Zero', side='ATK')

    def create_default_admin_user(apps, schema_editor):
        # Create default admin user
        # Username: admin
        # Password: caster_dashboard_2

        User = get_user_model()
        admin_user = User.objects.create_user("admin", None, "caster_dashboard_2")
        admin_user.is_staff = True
        admin_user.is_admin = True
        admin_user.is_superuser = True
        admin_user.save()

    dependencies = [
        ('dashboard', '0001_initial'),
        ('overlays', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_maps),
        migrations.RunPython(create_map_pools),
        migrations.RunPython(create_bomb_spots),
        migrations.RunPython(create_operators),
        migrations.RunPython(create_default_admin_user)
    ]
