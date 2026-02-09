from django.urls import path

from . import views

app_name = 'classifications'

urlpatterns = [
    path('', views.platform_list, name='platform-list'),
    path('add/', views.add_platform, name='add-platform'),
    path('<int:pk_platform>/', views.platform_detail, name='platform-detail'),
    path('<int:pk_platform>/delete/', views.delete_platform, name='delete-platform'),
    path('<int:pk_platform>/edit/', views.edit_platform, name='edit-platform'),
]
