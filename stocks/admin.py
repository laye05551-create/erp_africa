from django.contrib import admin
from .models import Categorie, Produit, MouvementStock

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    search_fields = ['nom']

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'categorie', 'prix_achat', 
                    'prix_vente', 'stock_actuel', 'stock_minimum', 'en_rupture']
    list_filter = ['categorie']
    search_fields = ['code', 'nom']

@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ['date', 'produit', 'type_mouvement', 'quantite', 'motif']
    list_filter = ['type_mouvement', 'date']
    search_fields = ['produit__nom', 'motif']