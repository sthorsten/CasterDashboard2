from django.contrib.auth import get_user_model
from django.test import TestCase

from dashboard.models.models import Profile


class TestAutoCreatedEntries(TestCase):
    def set_up(self):
        get_user_model().objects.create_user("testcaseuser", "testcaseuserpass")

    def test_profile_entry(self):
        user = get_user_model().objects.get(username="testcaseuser")
        entry = Profile.objects.get(user=user)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.confirmed, False)
