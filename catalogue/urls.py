"""reservations.catalogue URL Configuration
"""
from django.urls import path
from django.contrib import admin
from . import views
from .models import Artist

app_name='catalogue'

urlpatterns = [
    path('artist/', views.index, name='artist-index'),
    path('artist/<int:artist_id>', views.show, name='artist-show'),
    path('artist/edit/<int:artist_id>', views.artist.edit, name='artist-edit'),
    path('artist/create',views.artist.create, name='artist-create'),
    path('artist/delete/<int:artist_id>',views.artist.delete, name='artist-delete'),
    path('type/', views.type.index, name='type-index'),
    path('type/<int:type_id>' , views.type.show, name='type-show'),
    path('price/', views.price.index, name='price-index'),
    path('price/<int:price_id>', views.price.show, name='price-show'),
    path('locality/', views.locality.index, name='locality-index'),
    path('locality/<int:locality_id>', views.locality.show, name='locality-show'),
    path('location/', views.location.index, name='location-index'),
    path('location/<int:location_id>', views.location.show, name='location-show'),
]
