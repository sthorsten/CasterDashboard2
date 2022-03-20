from django.db import models


class Notification(models.Model):
    """Global notifications and alerts for all users"""

    TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('SUCCESS', 'Success'),
        ('WARN', 'Warning'),
        ('DANGER', 'Danger')
    ]

    title = models.CharField(max_length=255)
    text = models.TextField()
    type = models.CharField(
        max_length=255, choices=TYPE_CHOICES, default='INFO')

    show = models.BooleanField(default=True)
    showUntil = models.DateTimeField(
        null=True, blank=True, verbose_name="show until")

    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name="last modified")

    def __str__(self) -> str:
        return str(self.title)

    def __repr__(self) -> str:
        return f'<Notification {self.title}>'

    class Meta:
        verbose_name = "Notification"


class MapPool(models.Model):
    """ A collection of maps (e.g. Competetive, Ranked, Casual Map Pool) """

    name = models.CharField(max_length=255)
    maps = models.ManyToManyField('Map')

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<MapPool {self.name}>'

    class Meta:
        verbose_name = "Map Pool"


class Map(models.Model):
    """Represents a map in Rainbow Six Siege"""

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='maps', null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Map {self.name}>'

    class Meta:
        verbose_name = "Map"


class BombSpot(models.Model):
    """Represents a bomb spot location in Rainbow Six Siege"""

    FLOOR_CHOICES = [
        ('B', 'Basement'),
        ('B/1F', 'Basement / First Floor'),
        ('1F', 'First Floor'),
        ('1F/2F', 'First / Second Floor'),
        ('2F', 'Second Floor'),
        ('2F/3F', 'Second / Third Floor'),
        ('3F', 'Third Floor')
    ]

    map = models.ForeignKey(
        'Map', on_delete=models.CASCADE)
    floor = models.CharField(max_length=5, choices=FLOOR_CHOICES, default='1F')
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name} ({self.map})'

    def __repr__(self) -> str:
        return f'<BombSpot map={self.map} floor={self.floor} name={self.name}>'

    class Meta:
        verbose_name = "Bomb Spot"


class Operator(models.Model):
    """Represents an Operator in Rainbow Six Siege"""

    SIDE_CHOICES = [
        ('ATK', 'Attacker'),
        ('DEF', 'Defender')
    ]

    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    side = models.CharField(max_length=3, choices=SIDE_CHOICES)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Operator {self.name}>'
