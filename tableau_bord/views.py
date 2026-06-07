from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from comptabilite.models import CompteComptable, EcritureComptable
from stocks.models import Produit, MouvementStock
from facturation.models import Facture, Client

@login_required
def dashboard(request):
    # Statistiques générales
    total_clients = Client.objects.count()
    total_produits = Produit.objects.count()
    total_factures = Facture.objects.count()
    
    # Factures par statut
    factures_brouillon = Facture.objects.filter(statut='BR').count()
    factures_payees = Facture.objects.filter(statut='PY').count()
    factures_envoyees = Facture.objects.filter(statut='EN').count()
    
    # Produits en rupture de stock
    produits_rupture = Produit.objects.filter(
        stock_actuel__lte=models.F('stock_minimum')
    ) if False else [p for p in Produit.objects.all() if p.en_rupture]
    
    # Dernières factures
    dernieres_factures = Facture.objects.all()[:5]
    
    context = {
        'total_clients': total_clients,
        'total_produits': total_produits,
        'total_factures': total_factures,
        'factures_brouillon': factures_brouillon,
        'factures_payees': factures_payees,
        'factures_envoyees': factures_envoyees,
        'produits_rupture': produits_rupture,
        'dernieres_factures': dernieres_factures,
    }
    
    return render(request, 'tableau_bord/dashboard.html', context)