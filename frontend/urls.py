from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('shows/', views.show_list, name='show_list'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/<slug:slug>/', views.location_detail, name='location_detail'),
    path('a-propos/', views.about_us, name='about_us'),
]
