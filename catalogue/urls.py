"""reservations.catalogue URL Configuration
"""
from django.urls import path

from . import views

app_name='catalogue'

urlpatterns = [
    path('artist/', views.artist.index, name='artist-index'),
    path('artist/<int:artist_id>', views.artist.show, name='artist-show'),
    path('artist/edit/<int:artist_id>', views.artist.edit, name='artist-edit'),
    path('artist/create', views.artist.create, name='artist-create'),
    path('artist/delete/<int:artist_id>', views.artist.delete, name='artist-delete'),
    path('type/', views.type.index, name='type-index'),
    path('type/<int:type_id>', views.type.show, name='type-show'),
    path('type/create', views.type.create, name='type-create'),
    path('type/edit/<int:type_id>', views.type.edit, name='type-edit'),
    path('type/delete/<int:type_id>', views.type.delete, name='type-delete'),
    path('locality/', views.locality.index, name='locality-index'),
    path('locality/<int:locality_id>', views.locality.show, name='locality-show'),
    path('locality/create', views.locality.create, name='locality-create'),
    path('locality/edit/<int:locality_id>', views.locality.edit, name='locality-edit'),
    path('locality/delete/<int:locality_id>', views.locality.delete, name='locality-delete'),
    path('price/', views.price.index, name='price-index'),
    path('price/<int:price_id>', views.price.show, name='price-show'),
    path('price/create', views.price.create, name='price-create'),
    path('price/edit/<int:price_id>', views.price.edit, name='price-edit'),
    path('price/delete/<int:price_id>', views.price.delete, name='price-delete'),
    path('location/', views.location.index, name='location-index'),
    path('location/<int:location_id>', views.location.show, name='location-show'),
    path('location/create', views.location.create, name='location-create'),
    path('location/edit/<int:location_id>', views.location.edit, name='location-edit'),
    path('location/delete/<int:location_id>', views.location.delete, name='location-delete'),
    path('show/', views.show_.index, name='show-index'),
    path('show/<int:show_id>', views.show_.show, name='show-show'),
    path('show/create', views.show_.create, name='show-create'),
    path('show/edit/<int:show_id>', views.show_.edit, name='show-edit'),
    path('show/delete/<int:show_id>', views.show_.delete, name='show-delete'),
    path('representation/', views.representation.index, name='representation-index'),
    path('representation/<int:representation_id>', views.representation.show, name='representation-show'),
    path('representation/create', views.representation.create, name='representation-create'),
    path('representation/edit/<int:representation_id>', views.representation.edit, name='representation-edit'),
    path('representation/delete/<int:representation_id>', views.representation.delete, name='representation-delete'),
    path('review/', views.review.index, name='review-index'),
    path('review/<int:review_id>', views.review.show, name='review-show'),
    path('review/create', views.review.create, name='review-create'),
    path('review/edit/<int:review_id>', views.review.edit, name='review-edit'),
    path('review/delete/<int:review_id>', views.review.delete, name='review-delete'),
]
