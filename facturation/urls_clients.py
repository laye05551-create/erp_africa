from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_clients, name='liste_clients'),
    path('ajouter/', views.ajouter_client, name='ajouter_client'),
    path('modifier/<int:client_id>/', views.modifier_client, name='modifier_client'),
    path('supprimer/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
]