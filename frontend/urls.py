from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('shows/', views.show_list, name='show_list'),
    path('shows/<int:pk>/', views.show_detail, name='show_detail'),
    path('locations/', views.location_list, name='location_list'),
]
