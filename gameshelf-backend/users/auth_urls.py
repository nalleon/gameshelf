from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('register/', views.user_register),

    # verify email
    path('verify-email/', views.send_verification_email),
    path('verify-email/<uuid:token>/', views.verify_email),

    # password reset
    path('password-reset/', views.request_password_reset),
    path('change-password/', views.change_password),

    # activation
    path('activate/', views.send_activation_email),
    path('activate/<uuid:token>/', views.restore_account),

    # account
    path('deactivate/', views.deactivate_account),
]