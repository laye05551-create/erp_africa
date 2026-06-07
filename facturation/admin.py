from django.contrib import admin
from .models import Client, Facture, LigneFacture

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'telephone', 'email', 'adresse', 'ninea']
    search_fields = ['nom', 'telephone', 'email']

class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'date_emission', 
                    'date_echeance', 'statut', 'total_ttc']
    list_filter = ['statut', 'date_emission']
    search_fields = ['numero', 'client__nom']
    inlines = [LigneFactureInline]

@admin.register(LigneFacture)
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ['facture', 'produit', 'quantite', 'prix_unitaire', 'total']