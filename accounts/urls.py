from django.urls import path
from .views import UserSignUpView, UserUpdateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
]
