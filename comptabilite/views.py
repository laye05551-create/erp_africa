from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from entreprises.models import MembreEntreprise, Entreprise
from .models import CompteComptable, Journal, EcritureComptable

def get_entreprise(request):
    if request.user.is_superuser:
        return Entreprise.objects.first()
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.entreprise
    except MembreEntreprise.DoesNotExist:
        return None

@login_required
def liste_comptes(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    comptes = CompteComptable.objects.all()
    return render(request, 'comptabilite/comptes.html', {
        'comptes': comptes,
        'entreprise': entreprise
    })

@login_required
def liste_ecritures(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    ecritures = EcritureComptable.objects.all()
    return render(request, 'comptabilite/ecritures.html', {
        'ecritures': ecritures,
        'entreprise': entreprise
    })

@login_required
def ajouter_ecriture(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    comptes = CompteComptable.objects.all()
    journaux = Journal.objects.all()
    
    if request.method == 'POST':
        journal_id = request.POST.get('journal')
        date = request.POST.get('date')
        numero_piece = request.POST.get('numero_piece')
        libelle = request.POST.get('libelle')
        compte_id = request.POST.get('compte')
        debit = request.POST.get('debit') or 0
        credit = request.POST.get('credit') or 0
        
        journal = get_object_or_404(Journal, id=journal_id)
        compte = get_object_or_404(CompteComptable, id=compte_id)
        
        EcritureComptable.objects.create(
            journal=journal,
            date=date,
            numero_piece=numero_piece,
            libelle=libelle,
            compte=compte,
            debit=debit,
            credit=credit,
        )
        messages.success(request, 'Écriture ajoutée avec succès !')
        return redirect('/comptabilite/')
    
    return render(request, 'comptabilite/ajouter_ecriture.html', {
        'comptes': comptes,
        'journaux': journaux,
        'entreprise': entreprise
    })