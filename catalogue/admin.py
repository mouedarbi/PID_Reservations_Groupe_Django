from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Artist, ArtistType, ArtistTypeShow, Locality, Location, 
    Price, Representation, Reservation, RepresentationReservation, Review, Show, Type, UserMeta, ShowPrice,
    Affiliate, AffiliateTier
)

# Custom Admin classes with Import/Export support
@admin.register(Artist)
class ArtistAdmin(ImportExportModelAdmin):
    list_display = ('id', 'firstname', 'lastname')

@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'designation', 'locality', 'capacity')

@admin.register(Show)
class ShowAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'location', 'status')
    list_filter = ('status', 'location')

@admin.register(Representation)
class RepresentationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'show', 'schedule', 'location', 'available_seats')
    list_filter = ('schedule', 'location')

# Other models registration
admin.site.register(ArtistType)
admin.site.register(ArtistTypeShow)
admin.site.register(Locality)
admin.site.register(Price)
admin.site.register(RepresentationReservation)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(ShowPrice)
admin.site.register(Type)
admin.site.register(Affiliate)
admin.site.register(AffiliateTier)

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
