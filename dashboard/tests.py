from django.contrib.auth.models import User
from django.test import TestCase

from dashboard.models import Profile


class TestAutoCreatedEntries(TestCase):
    def setUp(self):
        User.objects.create_user("testcaseuser", "testcaseuserpass")

    def testProfileEntry(self):
        user = User.objects.get(username="testcaseuser")
        entry = Profile.objects.get(user=user)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.confirmed, False)


