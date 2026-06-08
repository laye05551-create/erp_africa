from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from comptabilite.models import CompteComptable
from stocks.models import Produit
from facturation.models import Facture, Client

@login_required
def dashboard(request):
    total_clients = Client.objects.count()
    total_produits = Produit.objects.count()
    total_factures = Facture.objects.count()
    
    factures_brouillon = Facture.objects.filter(statut='BR').count()
    factures_payees = Facture.objects.filter(statut='PY').count()
    factures_envoyees = Facture.objects.filter(statut='EN').count()
    
    produits_rupture = [p for p in Produit.objects.all() if p.en_rupture]
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