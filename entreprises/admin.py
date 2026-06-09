from django.contrib import admin
from .models import Entreprise, MembreEntreprise

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'telephone', 'email', 'ville', 'actif', 'date_creation']
    list_filter = ['actif', 'ville']
    search_fields = ['nom', 'email', 'ninea']

@admin.register(MembreEntreprise)
class MembreEntrepriseAdmin(admin.ModelAdmin):
    list_display = ['user', 'entreprise', 'role', 'actif']
    list_filter = ['role', 'actif', 'entreprise']
    search_fields = ['user__username', 'entreprise__nom']