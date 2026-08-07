# ============================================
# ERP Africa — Module IA d'analyse de données
# 100% gratuit — Python + Pandas + NumPy
# ============================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone


def analyser_entreprise(entreprise):
    """
    Analyse complète des données d'une entreprise
    Retourne des recommandations intelligentes
    """
    from facturation.models import Facture, LigneFacture
    from stocks.models import Produit
    from facturation.models import Client

    recommandations = []
    alertes = []
    statistiques = {}

    # ─── 1. ANALYSE DES STOCKS ───────────────────────────────────────────
    produits = Produit.objects.filter(entreprise=entreprise)
    
    if produits.exists():
        # Produits en rupture
        ruptures = [p for p in produits if p.en_rupture]
        if ruptures:
            for p in ruptures:
                alertes.append({
                    'type': 'danger',
                    'icone': '📦',
                    'message': f'Rupture de stock : {p.nom} — Stock actuel : {p.stock_actuel} (minimum : {p.stock_minimum})'
                })

        # Valeur totale du stock
        valeur_stock = sum(float(p.valeur_stock) for p in produits)
        statistiques['valeur_stock'] = valeur_stock
        statistiques['nombre_produits'] = produits.count()
        statistiques['produits_rupture'] = len(ruptures)

        # Produit le plus cher
        produit_plus_cher = produits.order_by('-prix_vente').first()
        if produit_plus_cher:
            statistiques['produit_plus_cher'] = produit_plus_cher.nom

    # ─── 2. ANALYSE DES FACTURES ─────────────────────────────────────────
    factures = Facture.objects.filter(entreprise=entreprise, est_supprime=False)
    
    if factures.exists():
        # Chiffre d'affaires total
        ca_total = sum(float(f.total_ttc) for f in factures if f.statut == 'PY')
        statistiques['ca_total'] = ca_total

        # Factures impayées
        factures_impayees = factures.filter(statut__in=['BR', 'EN'])
        montant_impaye = sum(float(f.total_ttc) for f in factures_impayees)
        statistiques['montant_impaye'] = montant_impaye
        statistiques['nombre_factures_impayees'] = factures_impayees.count()

        if montant_impaye > 0:
            alertes.append({
                'type': 'warning',
                'icone': '💸',
                'message': f'{factures_impayees.count()} facture(s) non payée(s) — Montant total : {montant_impaye:,.0f} FCFA'
            })

        # Taux de paiement
        total_factures = factures.count()
        factures_payees = factures.filter(statut='PY').count()
        if total_factures > 0:
            taux_paiement = (factures_payees / total_factures) * 100
            statistiques['taux_paiement'] = round(taux_paiement, 1)

            if taux_paiement < 50:
                recommandations.append({
                    'type': 'warning',
                    'icone': '💡',
                    'message': f'Taux de paiement faible ({taux_paiement:.0f}%) — Relancez vos clients pour les factures impayées'
                })

    # ─── 3. ANALYSE DES CLIENTS ──────────────────────────────────────────
    clients = Client.objects.filter(entreprise=entreprise)
    statistiques['nombre_clients'] = clients.count()

    if clients.count() == 0:
        recommandations.append({
            'type': 'info',
            'icone': '👥',
            'message': 'Ajoutez vos premiers clients pour commencer à facturer'
        })
    elif clients.count() < 5:
        recommandations.append({
            'type': 'info',
            'icone': '👥',
            'message': f'Vous avez {clients.count()} client(s) — Essayez d\'en acquérir davantage pour augmenter vos revenus'
        })

    # ─── 4. ANALYSE DES PRODUITS LES PLUS VENDUS ─────────────────────────
    from django.db.models import Sum, Count
    from facturation.models import LigneFacture

    top_produits = LigneFacture.objects.filter(
        facture__entreprise=entreprise,
        facture__est_supprime=False
    ).values(
        'produit__nom'
    ).annotate(
        total_vendu=Sum('quantite'),
        nombre_ventes=Count('id')
    ).order_by('-total_vendu')[:3]

    statistiques['top_produits'] = list(top_produits)

    if top_produits:
        meilleur = top_produits[0]
        recommandations.append({
            'type': 'success',
            'icone': '🏆',
            'message': f'Votre produit le plus vendu est "{meilleur["produit__nom"]}" avec {meilleur["total_vendu"]} unités vendues'
        })

    # ─── 5. RECOMMANDATIONS GENERALES ────────────────────────────────────
    if produits.exists() and clients.exists() and factures.exists():
        # Marge moyenne
        marges = []
        for p in produits:
            if p.prix_achat > 0:
                marge = ((p.prix_vente - p.prix_achat) / p.prix_achat) * 100
                marges.append(marge)
        
        if marges:
            marge_moyenne = np.mean(marges)
            statistiques['marge_moyenne'] = round(marge_moyenne, 1)
            
            if marge_moyenne < 20:
                recommandations.append({
                    'type': 'warning',
                    'icone': '📊',
                    'message': f'Marge moyenne faible ({marge_moyenne:.0f}%) — Considérez d\'augmenter vos prix de vente'
                })
            elif marge_moyenne > 50:
                recommandations.append({
                    'type': 'success',
                    'icone': '📊',
                    'message': f'Excellente marge moyenne de {marge_moyenne:.0f}% — Continuez ainsi !'
                })

    return {
        'recommandations': recommandations,
        'alertes': alertes,
        'statistiques': statistiques
    }