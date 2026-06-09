from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Entreprise, MembreEntreprise

def inscription(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom_entreprise = request.POST.get('nom_entreprise')
        ville = request.POST.get('ville')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Vérifications
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'entreprises/inscription.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà.')
            return render(request, 'entreprises/inscription.html')

        # Créer l'entreprise
        entreprise = Entreprise.objects.create(
            nom=nom_entreprise,
            ville=ville,
            telephone=telephone,
            email=email,
        )

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        # Lier l'utilisateur à l'entreprise
        MembreEntreprise.objects.create(
            user=user,
            entreprise=entreprise,
            role='AD',
        )

        messages.success(request, 'Compte créé avec succès ! Connectez-vous.')
        return redirect('/')

    return render(request, 'entreprises/inscription.html')