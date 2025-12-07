from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Add your API endpoints here
    path('', views.index, name='index'),
]