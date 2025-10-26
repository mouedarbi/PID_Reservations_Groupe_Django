from django.urls import path
from .views import UserSignUpView

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
]
