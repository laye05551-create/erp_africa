from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from entreprises.models import MembreEntreprise
from .models import Produit, Categorie, MouvementStock
from entreprises.models import MembreEntreprise, Entreprise

def get_entreprise(request):
    if request.user.is_superuser:
        return Entreprise.objects.first()
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.entreprise
    except MembreEntreprise.DoesNotExist:
        return None

@login_required
def liste_produits(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/erp-admin-secret/')
    produits = Produit.objects.filter(entreprise=entreprise)
    return render(request, 'stocks/produits.html', {
        'produits': produits,
        'entreprise': entreprise
    })

@login_required
def ajouter_produit(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/erp-admin-secret/')
    
    categories = Categorie.objects.filter(entreprise=entreprise)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        categorie_id = request.POST.get('categorie')
        prix_achat = request.POST.get('prix_achat')
        prix_vente = request.POST.get('prix_vente')
        stock_actuel = request.POST.get('stock_actuel')
        stock_minimum = request.POST.get('stock_minimum')
        unite = request.POST.get('unite')

        categorie = get_object_or_404(Categorie, id=categorie_id)
        
        Produit.objects.create(
            entreprise=entreprise,
            code=code,
            nom=nom,
            categorie=categorie,
            prix_achat=prix_achat,
            prix_vente=prix_vente,
            stock_actuel=stock_actuel,
            stock_minimum=stock_minimum,
            unite=unite,
        )
        messages.success(request, 'Produit ajouté avec succès !')
        return redirect('/stocks/')

    return render(request, 'stocks/ajouter_produit.html', {
        'categories': categories,
        'entreprise': entreprise
    })