from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from entreprises.models import MembreEntreprise, Entreprise
from .models import Client, Facture, LigneFacture
from stocks.models import Produit
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def get_entreprise(request):
    if request.user.is_superuser:
        return Entreprise.objects.order_by('id').first()
    try:
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.entreprise
    except MembreEntreprise.DoesNotExist:
        return None

def get_role(request):
    if request.user.is_superuser:
        return 'AD'
    try:
        from entreprises.models import MembreEntreprise
        membre = MembreEntreprise.objects.get(user=request.user)
        return membre.role
    except MembreEntreprise.DoesNotExist:
        return None

@login_required
def liste_clients(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    clients = Client.objects.filter(entreprise=entreprise)
    return render(request, 'facturation/clients.html', {
        'clients': clients,
        'entreprise': entreprise
    })

@login_required
def ajouter_client(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    if request.method == 'POST':
        Client.objects.create(
            entreprise=entreprise,
            nom=request.POST.get('nom'),
            telephone=request.POST.get('telephone'),
            email=request.POST.get('email'),
            adresse=request.POST.get('adresse'),
            ninea=request.POST.get('ninea'),
        )
        messages.success(request, 'Client ajouté avec succès !')
        return redirect('/clients/')
    return render(request, 'facturation/ajouter_client.html', {
        'entreprise': entreprise
    })
@login_required
def liste_factures(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    role = get_role(request)
    if role not in ['AD', 'CM', 'CO']:
        messages.error(request, 'Accès refusé.')
        return redirect('/dashboard/')
    factures = Facture.objects.filter(entreprise=entreprise, est_supprime=False)
    return render(request, 'facturation/factures.html', {
        'factures': factures,
        'entreprise': entreprise,
        'role': role
    })

@login_required
def ajouter_facture(request):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    clients = Client.objects.filter(entreprise=entreprise)
    produits = Produit.objects.filter(entreprise=entreprise)
    if request.method == 'POST':
        client_id = request.POST.get('client')
        numero = request.POST.get('numero')
        date_echeance = request.POST.get('date_echeance')
        client = get_object_or_404(Client, id=client_id)
        facture = Facture.objects.create(
            entreprise=entreprise,
            client=client,
            numero=numero,
            date_echeance=date_echeance,
            statut='BR',
        )
        produit_ids = request.POST.getlist('produit')
        quantites = request.POST.getlist('quantite')
        prix = request.POST.getlist('prix_unitaire')
        for i in range(len(produit_ids)):
            if produit_ids[i]:
                produit = get_object_or_404(Produit, id=produit_ids[i])
                LigneFacture.objects.create(
                    facture=facture,
                    produit=produit,
                    quantite=quantites[i],
                    prix_unitaire=prix[i],
                )
        messages.success(request, 'Facture créée avec succès !')
        return redirect('/factures/')
    return render(request, 'facturation/ajouter_facture.html', {
        'clients': clients,
        'produits': produits,
        'entreprise': entreprise
    })

@login_required
def generer_pdf(request, facture_id):
    entreprise = get_entreprise(request)
    facture = get_object_or_404(Facture, id=facture_id, entreprise=entreprise)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Facture_{facture.numero}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    titre_style = ParagraphStyle(
        'titre',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=20
    )
    elements.append(Paragraph(f"🌍 {entreprise.nom}", titre_style))
    elements.append(Paragraph(f"<b>FACTURE N° {facture.numero}</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.5*cm))
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
    elements.append(Paragraph("<b>CLIENT</b>", styles['Heading3']))
    elements.append(Paragraph(facture.client.nom, styles['Normal']))
    elements.append(Paragraph(facture.client.telephone, styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))
    data = [['Produit', 'Quantité', 'Prix Unitaire', 'Total']]
    for ligne in facture.lignes.all():
        data.append([
            ligne.produit.nom,
            str(ligne.quantite),
            f"{ligne.prix_unitaire:,.0f} FCFA",
            f"{ligne.total:,.0f} FCFA",
        ])
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
    elements.append(Paragraph(
        f"Merci pour votre confiance — {entreprise.nom} | {entreprise.ville}, Sénégal",
        styles['Normal']
    ))
    doc.build(elements)
    return response
@login_required
def modifier_client(request, client_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    client = get_object_or_404(Client, id=client_id, entreprise=entreprise)
    
    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.telephone = request.POST.get('telephone')
        client.email = request.POST.get('email')
        client.adresse = request.POST.get('adresse')
        client.ninea = request.POST.get('ninea')
        client.save()
        messages.success(request, 'Client modifié avec succès !')
        return redirect('/clients/')
    
    return render(request, 'facturation/modifier_client.html', {
        'client': client,
        'entreprise': entreprise
    })

@login_required
def supprimer_client(request, client_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    client = get_object_or_404(Client, id=client_id, entreprise=entreprise)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé !')
        return redirect('/clients/')
    return render(request, 'facturation/supprimer_client.html', {
        'client': client,
        'entreprise': entreprise
    })

@login_required
def modifier_statut_facture(request, facture_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    facture = get_object_or_404(Facture, id=facture_id, entreprise=entreprise)
    if request.method == 'POST':
        facture.statut = request.POST.get('statut')
        facture.save()
        messages.success(request, 'Statut mis à jour !')
        return redirect('/factures/')
    return render(request, 'facturation/modifier_statut.html', {
        'facture': facture,
        'entreprise': entreprise
    })

@login_required
def supprimer_facture(request, facture_id):
    entreprise = get_entreprise(request)
    if not entreprise:
        return redirect('/')
    facture = get_object_or_404(Facture, id=facture_id, entreprise=entreprise)
    if request.method == 'POST':
        from django.utils import timezone
        facture.est_supprime = True
        facture.date_suppression = timezone.now()
        facture.save()
        messages.success(request, 'Facture supprimee (archivee).')
        return redirect('/factures/')
    return render(request, 'facturation/supprimer_facture.html', {
        'facture': facture,
        'entreprise': entreprise
    })    

