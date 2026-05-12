from django.db import models
from django.contrib.auth.models import User
from .location import *
from .price import Price
from .show_price import ShowPrice

class ShowManager(models.Manager):
    def get_by_natural_key(self, slug, created_in):
        return self.get(slug=slug, created_in=created_in)

class Show(models.Model):
    SHOW_STATUS = [
        ('pending', 'En attente'),
        ('published', 'Publié'),
    ]
    slug = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    duration = models.PositiveSmallIntegerField(null=True)
    created_in = models.PositiveSmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shows')
    bookable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    producer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submitted_shows')
    status = models.CharField(max_length=20, choices=SHOW_STATUS, default='pending')
    external_url = models.URLField(max_length=255, null=True, blank=True)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True, related_name='shows')

    artist_types = models.ManyToManyField(
        "ArtistType",
        through="ArtistTypeShow",
        related_name="shows",
    )
    prices = models.ManyToManyField(
        Price,
        through=ShowPrice,
        related_name="shows",
    )

    objects = ShowManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shows"
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "created_in"],
                name="unique_slug_created_in",
            ),
        ]
    
    def natural_key(self):
        return (self.slug, self.created_in)

    @property
    def price(self):
        """
        Return the minimum price among all associated prices for this show.
        """
        if self.prices.exists():
            return min(p.price for p in self.prices.all())
        return None

    @property
    def has_multiple_prices(self):
        """
        Return True if the show has more than one price associated.
        """
        return self.prices.count() > 1

    @property
    def next_representation_date(self):
        """
        Return the date of the next upcoming representation.
        """
        from django.utils import timezone
        next_rep = self.representations.filter(schedule__gte=timezone.now()).order_by('schedule').first()
        return next_rep.schedule if next_rep else None

