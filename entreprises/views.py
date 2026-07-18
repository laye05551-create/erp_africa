from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Entreprise, MembreEntreprise

def get_entreprise(request):
    if request.user.is_superuser:
        return Entreprise.objects.order_by('id').first()
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.entreprise
    except MembreEntreprise.DoesNotExist:
        return None

def get_role(request):
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.role
    except MembreEntreprise.DoesNotExist:
        return None

def inscription(request):
    if request.method == 'POST':
        nom_entreprise = request.POST.get('nom_entreprise')
        ville = request.POST.get('ville')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'entreprises/inscription.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà.')
            return render(request, 'entreprises/inscription.html')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà utilisé par un autre compte.')
            return render(request, 'entreprises/inscription.html')

        entreprise = Entreprise.objects.create(
            nom=nom_entreprise,
            ville=ville,
            telephone=telephone,
            email=email,
        )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        MembreEntreprise.objects.create(
            user=user,
            entreprise=entreprise,
            role='AD',
        )

        from django.core.mail import send_mail
        from django.conf import settings
        send_mail(
            subject=f'Nouvelle inscription — {nom_entreprise}',
            message=f'Une nouvelle entreprise vient de s\'inscrire sur ERP Africa !\n\nNom : {nom_entreprise}\nVille : {ville}\nTéléphone : {telephone}\nEmail : {email}\nUsername : {username}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

        login(request, user)
        messages.success(request, f'Bienvenue {nom_entreprise} ! Votre espace est prêt.')
        return redirect('/dashboard/')

    return render(request, 'entreprises/inscription.html')


@login_required
def liste_membres(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    
    # Seul l'admin peut gérer les membres
    if not request.user.is_superuser:
        role = get_role(request)
        if role != 'AD':
            messages.error(request, 'Accès refusé — Administrateur uniquement.')
            return redirect('/dashboard/')
    
    membres = MembreEntreprise.objects.filter(entreprise=entreprise)
    return render(request, 'entreprises/membres.html', {
        'membres': membres,
        'entreprise': entreprise
    })


@login_required
def ajouter_membre(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    
    if not request.user.is_superuser:
        role = get_role(request)
        if role != 'AD':
            messages.error(request, 'Accès refusé — Administrateur uniquement.')
            return redirect('/dashboard/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà.')
            return render(request, 'entreprises/ajouter_membre.html', {'entreprise': entreprise})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        MembreEntreprise.objects.create(
            user=user,
            entreprise=entreprise,
            role=role,
            actif=True,
        )

        messages.success(request, f'Membre {username} ajouté avec succès !')
        return redirect('/entreprises/membres/')

    return render(request, 'entreprises/ajouter_membre.html', {
        'entreprise': entreprise
    })


@login_required
def modifier_membre(request, membre_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    
    if not request.user.is_superuser:
        role = get_role(request)
        if role != 'AD':
            return redirect('/dashboard/')
    
    membre = get_object_or_404(MembreEntreprise, id=membre_id, entreprise=entreprise)
    
    if request.method == 'POST':
        membre.role = request.POST.get('role')
        membre.actif = request.POST.get('actif') == 'on'
        membre.save()
        messages.success(request, 'Membre modifié avec succès !')
        return redirect('/entreprises/membres/')
    
    return render(request, 'entreprises/modifier_membre.html', {
        'membre': membre,
        'entreprise': entreprise
    })