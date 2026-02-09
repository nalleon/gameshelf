from django.urls import path

from . import views

app_name = 'classifications'

urlpatterns = [
    path('', views.edition_list, name='edition-list'),
    path('add/', views.add_edition, name='add-edition'),
    path('<int:pk_edition>/', views.edition_detail, name='edition-detail'),
    path('<int:pk_edition>/delete/', views.delete_edition, name='delete-edition'),
    path('<int:pk_edition>/edit/', views.edit_edition, name='edit-edition'),
]
