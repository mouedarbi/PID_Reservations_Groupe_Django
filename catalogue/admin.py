from django.contrib import admin
from .models import Artist
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from catalogue.models import UserMeta

# Register your models here.
admin.site.register(Artist)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton

class UserMetaInLine(admin.StackedInline):
    model = UserMeta
    can_delete = False
    verbose_name_plural = 'User Meta'

# Define a new User admin
class UserMetaInline:
    pass


class UserAdmin(BaseUserAdmin):
    inlines = [UserMetaInLine]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
