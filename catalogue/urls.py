"""reservations.catalogue URL Configuration
"""
from django.urls import path
from . import views

app_name='catalogue'

urlpatterns = [
    path('artist/', views.index, name='artist-index'),
    path('artist/<int:artist_id>', views.show, name='artist-show'),
    path('artist/edit/<int:artist_id>', views.artist.edit, name='artist-edit'),
    path('artist/create',views.artist.create, name='artist-create'),
    path('artist/delet/<int:artist_id>',views.artist.delete, name='artist-delete'),
]
