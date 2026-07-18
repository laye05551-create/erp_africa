from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/ajouter/', views.ajouter_membre, name='ajouter_membre'),
    path('membres/modifier/<int:membre_id>/', views.modifier_membre, name='modifier_membre'),
]