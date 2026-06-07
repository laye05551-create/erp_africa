from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import Facture

@login_required
def generer_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    
    # Créer le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Facture_{facture.numero}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Style titre
    titre_style = ParagraphStyle(
        'titre',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=20
    )
    
    # En-tête
    elements.append(Paragraph("🌍 ERP Africa", titre_style))
    elements.append(Paragraph(f"<b>FACTURE N° {facture.numero}</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Infos facture
    infos = [
        ['Date émission:', str(facture.date_emission)],
        ['Date échéance:', str(facture.date_echeance)],
        ['Statut:', facture.get_statut_display()],
    ]
    
    table_infos = Table(infos, colWidths=[4*cm, 8*cm])
    table_infos.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('TEXTCOLOR', (0,0), (0,-1), colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(table_infos)
    elements.append(Spacer(1, 0.5*cm))
    
    # Infos client
    elements.append(Paragraph("<b>CLIENT</b>", styles['Heading3']))
    elements.append(Paragraph(facture.client.nom, styles['Normal']))
    elements.append(Paragraph(facture.client.telephone, styles['Normal']))
    if facture.client.adresse:
        elements.append(Paragraph(facture.client.adresse, styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Lignes de facture
    elements.append(Paragraph("<b>DÉTAIL DES PRESTATIONS</b>", styles['Heading3']))
    
    data = [['Produit', 'Quantité', 'Prix Unitaire', 'Total']]
    for ligne in facture.lignes.all():
        data.append([
            ligne.produit.nom,
            str(ligne.quantite),
            f"{ligne.prix_unitaire:,.0f} FCFA",
            f"{ligne.total:,.0f} FCFA",
        ])
    
    # Totaux
    data.append(['', '', 'Total HT:', f"{facture.total_ht:,.0f} FCFA"])
    data.append(['', '', 'TVA (18%):', f"{facture.tva:,.0f} FCFA"])
    data.append(['', '', 'TOTAL TTC:', f"{facture.total_ttc:,.0f} FCFA"])
    
    table = Table(data, colWidths=[8*cm, 3*cm, 4*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-4), 0.5, colors.grey),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E1F5EE')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 1*cm))
    
    # Pied de page
    elements.append(Paragraph(
        "Merci pour votre confiance — ERP Africa | Dakar, Sénégal",
        styles['Normal']
    ))
    
    doc.build(elements)
    return response