from django.contrib.auth.models import User
from django.test import TestCase

from overlays.models import *


class TestAutoCreatedOverlayEntries(TestCase):
    def setUp(self):
        User.objects.create_user("testcaseuser", "testcaseuserpass")

    def testOverlayStyleEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = OverlayStyle.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testOverlayStateEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = OverlayState.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testMatchOverlayDataEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = MatchOverlayData.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testPollOverlayDataEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = PollOverlayData.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testSocialOverlayDataEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = SocialOverlayData.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testTimerOverlayDataEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = TimerOverlayData.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testTickerOverlayDataEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = TickerOverlayData.objects.filter(user=user).first()
        self.assertIsNotNone(entry)

    def testNextMatchOverlayDataEntry(self):
        user = User.objects.filter(username="testcaseuser").first()
        entry = NextMatchOverlayData.objects.filter(user=user).first()
        self.assertIsNotNone(entry)
