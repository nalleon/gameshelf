from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('register/', views.user_register),

    # verify email
    path('verify-email/', views.send_verification_email),
    path('verify-email/validate/', views.verify_email),

    # password reset
    path('password-reset/', views.request_password_reset),
    path('password-reset/validate/', views.validate_password_reset_token),
    path('change-password/', views.change_password),

    # activation
    path('activate/', views.send_activation_email),
    path('activate/validate/', views.restore_account),

    # account
    path('deactivate/', views.deactivate_account),
]