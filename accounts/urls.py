from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserSignUpView, UserUpdateView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Custom User Management
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('profile/', views.profile, name='user-profile'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('profile/delete/<int:pk>/', views.delete, name='user-delete'),

    # Django Auth Views - Custom Templates
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # next_page is handled by settings.LOGOUT_REDIRECT_URL

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'), 
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), 
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'),
]