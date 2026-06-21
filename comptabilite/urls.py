from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_comptes, name='liste_comptes'),
    path('ecritures/', views.liste_ecritures, name='liste_ecritures'),
    path('ecriture/ajouter/', views.ajouter_ecriture, name='ajouter_ecriture'),
]