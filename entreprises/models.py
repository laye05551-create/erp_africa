from auditlog.registry import auditlog
from django.db import models
from django.contrib.auth.models import User

class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    ninea = models.CharField(max_length=20, blank=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, default='Dakar')
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class MembreEntreprise(models.Model):
    ROLE_CHOICES = [
        ('AD', 'Administrateur'),
        ('CO', 'Comptable'),
        ('MA', 'Magasinier'),
        ('CM', 'Commercial'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='CO')
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres de l'entreprise"

    def __str__(self):
        return f"{self.user.username} - {self.entreprise.nom} ({self.get_role_display()})"
        
auditlog.register(Entreprise)
auditlog.register(MembreEntreprise)