from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from entreprises.models import MembreEntreprise, Entreprise
from .models import Produit, Categorie

def get_entreprise(request):
    if request.user.is_superuser:
        return Entreprise.objects.order_by('id').first()
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        if not membre.actif:
            return None
        return membre.entreprise
    except MembreEntreprise.DoesNotExist:
        return None

def get_role(request):
    if request.user.is_superuser:
        return 'AD'
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.role
    except MembreEntreprise.DoesNotExist:
        return None
@login_required
def liste_produits(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    role = get_role(request)
    if role not in ['AD', 'MA']:
        messages.error(request, 'Accès refusé — Stocks réservé aux Administrateurs et Magasiniers.')
        return redirect('/dashboard/')
    produits = Produit.objects.filter(entreprise=entreprise)
    return render(request, 'stocks/produits.html', {
        'produits': produits,
        'entreprise': entreprise,
        'role': role
    })

@login_required
def ajouter_produit(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
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

@login_required
def liste_categories(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    categories = Categorie.objects.filter(entreprise=entreprise)
    return render(request, 'stocks/categories.html', {
        'categories': categories,
        'entreprise': entreprise
    })

@login_required
def ajouter_categorie(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        Categorie.objects.create(
            entreprise=entreprise,
            nom=nom,
            description=description,
        )
        messages.success(request, 'Catégorie ajoutée avec succès !')
        return redirect('/stocks/categories/')
    return render(request, 'stocks/ajouter_categorie.html', {
        'entreprise': entreprise
    })
@login_required
def modifier_produit(request, produit_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    produit = get_object_or_404(Produit, id=produit_id, entreprise=entreprise)
    categories = Categorie.objects.filter(entreprise=entreprise)
    
    if request.method == 'POST':
        produit.code = request.POST.get('code')
        produit.nom = request.POST.get('nom')
        produit.categorie = get_object_or_404(Categorie, id=request.POST.get('categorie'))
        produit.prix_achat = request.POST.get('prix_achat')
        produit.prix_vente = request.POST.get('prix_vente')
        produit.stock_actuel = request.POST.get('stock_actuel')
        produit.stock_minimum = request.POST.get('stock_minimum')
        produit.unite = request.POST.get('unite')
        produit.save()
        messages.success(request, 'Produit modifié avec succès !')
        return redirect('/stocks/')
    
    return render(request, 'stocks/modifier_produit.html', {
        'produit': produit,
        'categories': categories,
        'entreprise': entreprise
    })

@login_required
def supprimer_produit(request, produit_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    produit = get_object_or_404(Produit, id=produit_id, entreprise=entreprise)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé !')
        return redirect('/stocks/')
    return render(request, 'stocks/supprimer_produit.html', {
        'produit': produit,
        'entreprise': entreprise
    })