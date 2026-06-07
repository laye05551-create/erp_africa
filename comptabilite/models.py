from django.db import models

# ============================================
# MODULE COMPTABILITÉ SYSCOHADA
# ERP Africa — Mouhamadou Faye
# ============================================

class CompteComptable(models.Model):
    """Plan comptable SYSCOHADA"""
    
    CLASSE_CHOICES = [
        ('1', 'Classe 1 - Comptes de ressources durables'),
        ('2', 'Classe 2 - Comptes d\'actif immobilisé'),
        ('3', 'Classe 3 - Comptes de stocks'),
        ('4', 'Classe 4 - Comptes de tiers'),
        ('5', 'Classe 5 - Comptes de trésorerie'),
        ('6', 'Classe 6 - Comptes de charges'),
        ('7', 'Classe 7 - Comptes de produits'),
    ]

    numero = models.CharField(max_length=10, unique=True)
    libelle = models.CharField(max_length=200)
    classe = models.CharField(max_length=1, choices=CLASSE_CHOICES)
    solde_debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    solde_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Compte Comptable"
        verbose_name_plural = "Plan Comptable SYSCOHADA"
        ordering = ['numero']

    def __str__(self):
        return f"{self.numero} - {self.libelle}"

    @property
    def solde(self):
        return self.solde_debit - self.solde_credit


class Journal(models.Model):
    """Journaux comptables"""

    TYPE_CHOICES = [
        ('AC', 'Achats'),
        ('VT', 'Ventes'),
        ('BQ', 'Banque'),
        ('CA', 'Caisse'),
        ('OD', 'Opérations Diverses'),
    ]

    code = models.CharField(max_length=5, unique=True)
    libelle = models.CharField(max_length=100)
    type_journal = models.CharField(max_length=2, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journaux Comptables"

    def __str__(self):
        return f"{self.code} - {self.libelle}"


class EcritureComptable(models.Model):
    """Écritures comptables"""

    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    date = models.DateField()
    numero_piece = models.CharField(max_length=20)
    libelle = models.CharField(max_length=200)
    compte = models.ForeignKey(CompteComptable, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Écriture Comptable"
        verbose_name_plural = "Écritures Comptables"
        ordering = ['-date', 'numero_piece']

    def __str__(self):
        return f"{self.date} | {self.numero_piece} | {self.libelle}"
