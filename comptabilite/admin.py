from django.contrib import admin
from .models import CompteComptable, Journal, EcritureComptable

@admin.register(CompteComptable)
class CompteComptableAdmin(admin.ModelAdmin):
    list_display = ['numero', 'libelle', 'classe', 'solde_debit', 'solde_credit', 'actif']
    list_filter = ['classe', 'actif']
    search_fields = ['numero', 'libelle']

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['code', 'libelle', 'type_journal']
    search_fields = ['code', 'libelle']

@admin.register(EcritureComptable)
class EcritureComptableAdmin(admin.ModelAdmin):
    list_display = ['date', 'numero_piece', 'libelle', 'compte', 'debit', 'credit']
    list_filter = ['journal', 'date']
    search_fields = ['numero_piece', 'libelle']
    date_hierarchy = 'date'