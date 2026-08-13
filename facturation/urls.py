from django.urls import path
from . import views

urlpatterns = [
    # Génère l'URL : /factures/pdf/9/
    path('pdf/<int:facture_id>/', views.generer_pdf, name='generer_pdf'),
]