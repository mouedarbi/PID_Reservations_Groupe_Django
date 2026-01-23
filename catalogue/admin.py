from django.contrib import admin
from .models import (
    Artist,
    ArtistType,
    ArtistTypeShow,
    Locality,
    Location,
    Price,
    Representation,
    Reservation,
    Review,
    Show,
    Type,
    UserMeta,
)

# A simple registration for each model to make them appear in the admin
admin.site.register(Artist)
admin.site.register(ArtistType)
admin.site.register(ArtistTypeShow)
admin.site.register(Locality)
admin.site.register(Location)
admin.site.register(Price)
admin.site.register(Representation)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Show)
admin.site.register(Type)
admin.site.register(UserMeta)

