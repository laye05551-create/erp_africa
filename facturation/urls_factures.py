from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_factures, name='liste_factures'),
    path('ajouter/', views.ajouter_facture, name='ajouter_facture'),
    path('statut/<int:facture_id>/', views.modifier_statut_facture, name='modifier_statut'),
]