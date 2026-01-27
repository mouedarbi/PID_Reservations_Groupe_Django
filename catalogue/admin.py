from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Artist, ArtistType, ArtistTypeShow, Locality, Location, 
    Price, Representation, Reservation, Review, Show, Type, UserMeta
)

# Register your models here.
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

# UserMeta registration as inline with User
class UserMetaInLine(admin.StackedInline):
    model = UserMeta
    can_delete = False
    verbose_name_plural = 'User Meta'


class UserAdmin(BaseUserAdmin):
    inlines = [UserMetaInLine]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
