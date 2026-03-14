from django.urls import path

from . import views

# app_name = 'libraries'

urlpatterns = [
    path('', views.library_item_list, name='library-list'),
    path('add/', views.add_library_item, name='add-library'),
    path('<int:pk_library_item>/', views.library_item_detail, name='library-detail'),
    path('<int:pk_library_item>/delete/', views.delete_library_item, name='delete-library'),
    path('<int:pk_library_item>/edit/', views.edit_library_item, name='edit-library'),
]
