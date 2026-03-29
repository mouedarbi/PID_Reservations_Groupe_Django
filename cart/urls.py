from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:representation_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:representation_id>/<int:price_id>/', views.cart_remove, name='cart_remove'),
]
