from django.db import models
from entreprises.models import Entreprise

class Categorie(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Produit(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=15, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=15, decimal_places=2)
    stock_actuel = models.IntegerField(default=0)
    stock_minimum = models.IntegerField(default=5)
    unite = models.CharField(max_length=20, default='unité')

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']
        unique_together = ['entreprise', 'code']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @property
    def en_rupture(self):
        return self.stock_actuel <= self.stock_minimum

    @property
    def valeur_stock(self):
        return self.stock_actuel * self.prix_achat


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('EN', 'Entrée'),
        ('SO', 'Sortie'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    type_mouvement = models.CharField(max_length=2, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Mouvement de Stock"
        verbose_name_plural = "Mouvements de Stock"
        ordering = ['-date']

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} - {self.quantite}"