"""reservations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import include, path
from catalogue.views.admin_dashboard import (
    admin_dashboard, admin_show_index, admin_representation_index, 
    admin_artist_index, admin_type_index, admin_review_index, 
    admin_location_index, admin_locality_index, admin_reservation_index, 
    admin_reservation_detail, admin_user_index, admin_group_index,
    admin_price_index, admin_show_detail, admin_artist_create, admin_artist_edit,
    admin_artist_detail, admin_show_create, admin_show_edit
)


urlpatterns = [
    #path('', RedirectView.as_view(url='/artist/', permanent=False)),
    path('', include('frontend.urls')), # Added for frontend app

    # Custom Admin Dashboard
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/shows/', admin_show_index, name='admin_show_index'),
    path('admin-dashboard/shows/create/', admin_show_create, name='admin_show_create'),
    path('admin-dashboard/shows/<int:pk>/', admin_show_detail, name='admin_show_detail'),
    path('admin-dashboard/shows/<int:pk>/edit/', admin_show_edit, name='admin_show_edit'),
    path('admin-dashboard/representations/', admin_representation_index, name='admin_representation_index'),
    path('admin-dashboard/artists/', admin_artist_index, name='admin_artist_index'),
    path('admin-dashboard/artists/<int:pk>/', admin_artist_detail, name='admin_artist_detail'),
    path('admin-dashboard/artists/create/', admin_artist_create, name='admin_artist_create'),
    path('admin-dashboard/artists/<int:pk>/edit/', admin_artist_edit, name='admin_artist_edit'),
    path('admin-dashboard/types/', admin_type_index, name='admin_type_index'),
    path('admin-dashboard/reviews/', admin_review_index, name='admin_review_index'),
    path('admin-dashboard/locations/', admin_location_index, name='admin_location_index'),
    path('admin-dashboard/localities/', admin_locality_index, name='admin_locality_index'),
    path('admin-dashboard/reservations/', admin_reservation_index, name='admin_reservation_index'),
    path('admin-dashboard/reservations/<int:pk>/', admin_reservation_detail, name='admin_reservation_detail'),
    path('admin-dashboard/users/', admin_user_index, name='admin_user_index'),
    path('admin-dashboard/groups/', admin_group_index, name='admin_group_index'),
    path('admin-dashboard/prices/', admin_price_index, name='admin_price_index'),

    path('accounts/', include('accounts.urls')), # All accounts/auth related URLs will be handled here
    
    path('catalogue/', include('catalogue.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

