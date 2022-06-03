from django.test import TestCase
from .models import Notification, MapPool, Map, BombSpot, Operator


class NotificationTestCase(TestCase):
    def setUp(self) -> None:
        Notification.objects.create(
            title="TestNotification",
            text="This is a test notification",
            type="INFO"
        )

    def test_notification_name(self):
        notification = Notification.objects.get(title="TestNotification")
        self.assertEqual(str(notification), "TestNotification")
        self.assertEqual(repr(notification), "<Notification TestNotification>")


class MapPoolTestCase(TestCase):
    def setUp(self) -> None:
        MapPool.objects.create(name="TestMapPool")

    def test_mappool_name(self):
        mappool = MapPool.objects.get(name="TestMapPool")
        self.assertEqual(str(mappool), "TestMapPool")
        self.assertEqual(repr(mappool), "<MapPool TestMapPool>")


class MapTestCase(TestCase):
    def setUp(self) -> None:
        Map.objects.create(name="TestMap")

    def test_map_name(self):
        testmap = Map.objects.get(name="TestMap")
        self.assertEqual(str(testmap), "TestMap")
        self.assertEqual(repr(testmap), "<Map TestMap>")

    def test_map_to_all_mappool_receiver(self):
        all_map_pool = MapPool.objects.get(name="All")
        testmap = all_map_pool.maps.get(name="TestMap")
        self.assertIsNotNone(testmap)


class BombSpotTestCase(TestCase):
    def setUp(self) -> None:
        testmap = Map.objects.create(name="BombSpotTestMap")
        BombSpot.objects.create(floor="B", map=testmap, name="TestBombSpot")

    def test_bombspot_name(self):
        testbombspot = BombSpot.objects.get(name="TestBombSpot")
        self.assertEqual(str(testbombspot), "TestBombSpot (BombSpotTestMap)")
        self.assertEqual(
            repr(testbombspot), "<BombSpot map=BombSpotTestMap floor=B name=TestBombSpot>")


class OperatorTestCase(TestCase):
    def setUp(self) -> None:
        Operator.objects.create(name="TestOperator", side="ATK")

    def test_operator_name(self):
        operator = Operator.objects.get(name="TestOperator")
        self.assertEqual(str(operator), "TestOperator")
        self.assertEqual(repr(operator), "<Operator TestOperator>")
