from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from stocks.models import Produit
from facturation.models import Facture, Client
from entreprises.models import MembreEntreprise

@login_required
def dashboard(request):
    # Récupérer l'entreprise de l'utilisateur connecté
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        entreprise = membre.entreprise
    except MembreEntreprise.DoesNotExist:
        return redirect('/erp-admin-secret/')

    # Statistiques filtrées par entreprise
    total_clients = Client.objects.filter(entreprise=entreprise).count()
    total_produits = Produit.objects.filter(entreprise=entreprise).count()
    total_factures = Facture.objects.filter(entreprise=entreprise).count()

    factures_brouillon = Facture.objects.filter(entreprise=entreprise, statut='BR').count()
    factures_payees = Facture.objects.filter(entreprise=entreprise, statut='PY').count()
    factures_envoyees = Facture.objects.filter(entreprise=entreprise, statut='EN').count()

    produits_rupture = [p for p in Produit.objects.filter(entreprise=entreprise) if p.en_rupture]
    dernieres_factures = Facture.objects.filter(entreprise=entreprise)[:5]

    context = {
        'entreprise': entreprise,
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