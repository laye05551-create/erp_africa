from django.urls import path
from . import views

urlpatterns = [
    path('facture/<int:facture_id>/pdf/', views.generer_pdf, name='generer_pdf'),
]