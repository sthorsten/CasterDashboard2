from datetime import date, datetime
from django.db import models


class League(models.Model):
    """ Represents a league
        Leagues have their own management and logo to be displayed in the overlays
        Matches are usually first being categorized into leagues
    """

    name = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    customDesign = models.BooleanField(
        default=False, verbose_name="custom design")

    logo = models.ImageField(upload_to='leagues', null=True, blank=True)
    logoSmall = models.ImageField(
        upload_to='leagues', null=True, blank=True, verbose_name="small logo")

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name="last modified")

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<League {self.name}>'


class Season(models.Model):
    """ Represents either an official "generic" Rainbow Six Siege season (as released by Ubisoft)
        or a custom one for categorizing matches.
        A season can also be associated with a league to allow for even more detailed categorizing of matches
        as well as being able to restrict access to that season
    """

    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="You can leave this field blank. The season name will then be set automatically, e.g. 'Season 4'"
    )
    seasonNo = models.IntegerField(default=1, verbose_name="season number")
    league = models.ForeignKey(
        'League', on_delete=models.CASCADE, related_name='seasons')

    playdayCount = models.IntegerField(verbose_name="playday count")

    startDate = models.DateField(
        default=date.today, null=True, blank=True, verbose_name="start date")
    endDate = models.DateField(
        default=date.today, null=True, blank=True, verbose_name="end date")

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name="last modified")

    def __str__(self) -> str:
        # Include the league in brackets
        return f'{self.name} ({str(self.league)})'

    def __repr__(self) -> str:
        return f'<Season {self.name}>'


class Playday(models.Model):
    """Represents a playday containing matches being played during a season"""

    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="You can leave this field blank. The playday name will then be set automatically, e.g. 'Playday 4'"
    )
    season = models.ForeignKey(
        'Season', on_delete=models.CASCADE, related_name='playdays')
    playdayNo = models.IntegerField(default=1, verbose_name="playday number")
    date = models.DateField(default=date.today, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name="last modified")

    def __str__(self) -> str:
        # Include season & league in brackets
        return f'{self.name} ({self.season.league} - {self.season.name})'

    def __repr__(self) -> str:
        return f'<Playday {self.name}>'


class Tournament(models.Model):
    """Represents a tournament containing matches being played in a league"""

    name = models.CharField(max_length=255)
    league = models.ForeignKey(
        'League', on_delete=models.CASCADE, related_name='tournaments')

    startDate = models.DateField(default=date.today, null=True, blank=True)
    endDate = models.DateField(default=date.today, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name="last modified")

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Tournament {self.name}>'


class Sponsor(models.Model):
    """ Represents a sponsor, that are either available to all users or can be associated with a league
        Sponsor logos are displayed in various overlays
    """

    name = models.CharField(max_length=255)
    public = models.BooleanField(
        default=True,
        help_text="If checked, this sponsor will be available for all users"
    )
    league = models.ForeignKey(
        'League', on_delete=models.CASCADE, related_name='sponsors',
        null=True, blank=True,
        help_text="If set, the sponsor will always be selected when creating a match in the set league. Can be left blank")
    logo = models.ImageField(
        upload_to="sponsors", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Sponsor {self.name}>'


class Team(models.Model):
    """Represents a team that plays in matches"""

    name = models.CharField(max_length=22, unique=True)
    logo = models.ImageField(upload_to="teams", blank=True, null=True)
    logoSmall = models.ImageField(
        upload_to="teams", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Team {self.name}>'


class LeagueCustomization(models.Model):
    # ToDo: Add overlays - then add customization model fields
    '''
    startOverlay
    mapBanOverlay
    inGameOverlay
    opBansOverlay
    roundOverlay
    scheduleOverlay
    footerOverlay
    socialOverlay
    inGameMapsOverlay? - BO 2-5
    '''
