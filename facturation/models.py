from auditlog.registry import auditlog
from django.db import models
from entreprises.models import Entreprise

class Client(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    ninea = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Facture(models.Model):
    STATUT_CHOICES = [
        ('BR', 'Brouillon'),
        ('EN', 'Envoyée'),
        ('PY', 'Payée'),
        ('AN', 'Annulée'),
    ]

    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_emission = models.DateField(auto_now_add=True)
    date_echeance = models.DateField()
    statut = models.CharField(max_length=2, choices=STATUT_CHOICES, default='BR')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-date_emission']
        unique_together = ['entreprise', 'numero']

    def __str__(self):
        return f"Facture {self.numero} - {self.client.nom}"

    @property
    def total_ht(self):
        return sum(ligne.total for ligne in self.lignes.all())

    @property
    def tva(self):
        return self.total_ht * 18 / 100

    @property
    def total_ttc(self):
        return self.total_ht + self.tva


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('stocks.Produit', on_delete=models.PROTECT)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Ligne de Facture"
        verbose_name_plural = "Lignes de Facture"

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

    @property
    def total(self):
        return self.quantite * self.prix_unitaire

auditlog.register(Client)
auditlog.register(Facture)   