import logging
import uuid
from django.contrib.auth import get_user_model
from django.db import models
from main.models import League

logger = logging.getLogger(__name__)

User = get_user_model()


class Profile(models.Model):
    """The profile extends django's default user model to allow for a few extra fields"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')

    registrationToken = models.UUIDField(default=uuid.uuid4)
    accountConfirmed = models.BooleanField(default=False)
    emailConfirmed = models.BooleanField(default=False)

    # User definable role, such as Caster, Observer, Producer, etc.
    role = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)

    def __repr__(self) -> str:
        return f'<Profile {self.user}>'

    class Meta:
        verbose_name = "Profile"


class LeagueAccessGroup(models.Model):
    """Represents how a user can interact with a league"""

    PERMISSION_GROUPS = [
        # can select the league for new matches
        ('BASIC', 'Basic'),
        # can see all matches (read only) of the league
        ('REGULAR', 'Regular'),
        # can see and edit all matches of the league
        ('MANAGER', 'Manager'),
        # can additionally manage all league details (name, logo, etc.)
        ('ADMIN', 'Admin')
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='leagueAccessGroups')
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    permissionGroup = models.CharField(
        choices=PERMISSION_GROUPS, max_length=255)

    def __str__(self) -> str:
        return f'{str(self.user)}: {str(self.league)} ({self.permissionGroup})'  # pylint: disable=no-member

    def __repr__(self) -> str:
        return f'<LeagueGroup {self.user}>'

    class Meta:
        verbose_name = "League Group"
