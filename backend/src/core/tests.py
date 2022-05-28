from django.test import TestCase
from django.db.utils import DataError
from .models import Map, BombSpot


class MapTestCase(TestCase):
    def setUp(self):
        Map.objects.create(name="TestMap")

    def test_map_name(self):
        testmap = Map.objects.get(name="TestMap")
        self.assertEqual(str(testmap), "TestMap")
        self.assertEqual(repr(testmap), "<Map TestMap>")


class BombSpotTestCase(TestCase):
    def setUp(self) -> None:
        testmap = Map.objects.create(name="BombSpotTestMap")
        BombSpot.objects.create(floor="B", map=testmap, name="TestBombSpot")

    def test_bombspot_name(self):
        testbombspot = BombSpot.objects.get(name="TestBombSpot")
        self.assertEqual(str(testbombspot), "TestBombSpot (BombSpotTestMap)")
        self.assertEqual(
            repr(testbombspot), "<BombSpot map=BombSpotTestMap floor=B name=TestBombSpot>")

    def test_invalid_floor(self):
        testmap = Map.objects.get(name="BombSpotTestMap")
        with self.assertRaises(DataError):
            BombSpot.objects.create(floor="FloorNameTooLong",
                                    map=testmap, name="InvalidTestBombSpot")
