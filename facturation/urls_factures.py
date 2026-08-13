from django.urls import path
from . import views

urlpatterns = [
    # Liste des factures
    path('', views.liste_factures, name='liste_factures'),
    
    # Création / Ajout (support de deux alias)
    path('ajouter/', views.ajouter_facture, name='ajouter_facture'),
    path('creer/', views.ajouter_facture, name='creer_facture'),
    
    # Consultation et Édition
    path('detail/<int:facture_id>/', views.detail_facture, name='detail_facture'),
    path('modifier/<int:facture_id>/', views.modifier_facture, name='modifier_facture'),
    path('statut/<int:facture_id>/', views.modifier_statut_facture, name='modifier_statut'),
    path('supprimer/<int:facture_id>/', views.supprimer_facture, name='supprimer_facture'),
    
    # Exports & Impression
    path('pdf/<int:facture_id>/', views.generer_pdf, name='generer_pdf'),
    path('export/excel/', views.exporter_factures_excel, name='exporter_factures_excel'),
]