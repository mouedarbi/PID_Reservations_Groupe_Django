from django.urls import path
from .views import UserSignUpView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('profile/', views.profile, name='user-profile'),
]
