from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from .models import Entreprise, MembreEntreprise

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

        # Envoyer email de notification à l'admin
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