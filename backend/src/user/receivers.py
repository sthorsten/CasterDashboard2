import logging
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token
from overlays.models import UserOverlay
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
        UserOverlay.objects.create(user=instance)
