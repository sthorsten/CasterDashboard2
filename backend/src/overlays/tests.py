from django.contrib.auth import get_user_model
from django.test import TestCase

# from overlays.models.models import OverlayStyle, OverlayState, MatchOverlayData, PollOverlayData, \
#     SocialOverlayData, TimerOverlayData, TickerOverlayData


# class TestAutoCreatedOverlayEntries(TestCase):
#     def setUp(self):
#         get_user_model().objects.create_user("testcaseuser", "testcaseuserpass")

#     def testOverlayStyleEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = OverlayStyle.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)

#     def testOverlayStateEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = OverlayState.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)

#     def testMatchOverlayDataEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = MatchOverlayData.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)

#     def testPollOverlayDataEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = PollOverlayData.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)

#     def testSocialOverlayDataEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = SocialOverlayData.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)

#     def testTimerOverlayDataEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = TimerOverlayData.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)

#     def testTickerOverlayDataEntry(self):
#         user = get_user_model().objects.filter(username="testcaseuser").first()
#         entry = TickerOverlayData.objects.filter(user=user).first()
#         self.assertIsNotNone(entry)
