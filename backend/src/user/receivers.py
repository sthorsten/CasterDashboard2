import logging
import secrets
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token
from .models import Profile

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(signals.post_save, sender=User)
def new_user_post_save(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    # Create overlay entries when a new user is created

    if created:
        logger.info("New user. Creating additional data...")

        if instance.username == "admin":
            # Do not create any overlay data for the default admin user
            return

        Profile.objects.create(user=instance)
        Token.objects.get_or_create(user=instance)

        # OverlayStyle.objects.create(user=instance)
        # OverlayState.objects.create(user=instance)
        # MatchOverlayData.objects.create(user=instance)
        # PollOverlayData.objects.create(user=instance)
        # SocialOverlayData.objects.create(user=instance)
        # TimerOverlayData.objects.create(user=instance)
        # TickerOverlayData.objects.create(user=instance)
