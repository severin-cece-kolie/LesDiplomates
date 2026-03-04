from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Transaction, FraisScolarite
from .services import ComptaService
from apps.eleves.models import Eleve
from apps.accounts.permissions import finance_required

@login_required
@finance_required
def dashboard_finance(request):
    from django.db.models import Sum, Count
    from django.utils import timezone
    now = timezone.now()
    
    # KPIs
    recettes_mois = Transaction.objects.filter(
        statut='VALIDE', created_at__year=now.year, created_at__month=now.month
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    frais_impayes = FraisScolarite.objects.filter(est_solde=False)
    total_impaye = sum(f.montant_attendu - f.montant_paye for f in frais_impayes)
    nb_eleves_retard = frais_impayes.values('eleve').distinct().count()
    
    total_attendu = FraisScolarite.objects.aggregate(t=Sum('montant_attendu'))['t'] or 1
    total_paye = FraisScolarite.objects.aggregate(t=Sum('montant_paye'))['t'] or 0
    taux_recouvrement = round((total_paye / total_attendu) * 100) if total_attendu > 0 else 0
    
    recent_transactions = Transaction.objects.select_related('eleve').order_by('-created_at')[:5]
    
    methode_stats = Transaction.objects.filter(statut='VALIDE').values('methode').annotate(count=Count('id'), total=Sum('montant')).order_by('-total')
    methode_total = sum(m['count'] for m in methode_stats) or 1
    for m in methode_stats:
        m['pct'] = round((m['count'] / methode_total) * 100)
    
    activites = Transaction.objects.select_related('eleve', 'enregistre_par').order_by('-created_at')[:5]
    
    return render(request, 'dashboards/finance/index.html', {
        'recent_transactions': recent_transactions,
        'recettes_mois': recettes_mois,
        'total_impaye': total_impaye,
        'nb_eleves_retard': nb_eleves_retard,
        'taux_recouvrement': taux_recouvrement,
        'methode_stats': methode_stats,
        'activites': activites,
        'mois_actuel': now.strftime('%B %Y'),
    })

@login_required
@finance_required
def liste_transactions(request):
    transactions = Transaction.objects.order_by('-created_at')
    return render(request, 'pages/finance/transactions.html', {'transactions': transactions})

@login_required
@finance_required
def transaction_validation(request, transaction_id):
    """Page de validation d'une transaction spécifique"""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'pages/finance/transaction_detail.html', {'transaction': transaction})

@login_required
def payment_checkout(request):
    """Page de paiement pour parents/élèves"""
    if not request.user.is_parent() and not request.user.is_eleve():
        return render(request, 'errors/403.html', status=403)
    
    # Charger les frais de l'élève concerné
    from apps.eleves.models import Eleve
    enfant = None
    frais = []
    if request.user.is_parent() and hasattr(request.user, 'profil_parent'):
        enfant_id = request.GET.get('eleve')
        enfants = request.user.profil_parent.enfants.all()
        enfant = enfants.filter(id=enfant_id).first() or enfants.first()
        if enfant:
            frais = FraisScolarite.objects.filter(eleve=enfant, est_solde=False)
    return render(request, 'pages/paiement.html', {'enfant': enfant, 'frais': frais})

@login_required
def payment_confirmation(request):
    """Page de confirmation après paiement réussi"""
    return render(request, 'pages/paiement_succes.html')

@login_required
@finance_required
def enregistrement_manuel(request):
    if request.method == 'POST':
# ... (rest of the code remains the same but using the decorator)
        eleve_id = request.POST.get('eleve_id')
        montant = request.POST.get('montant')
        methode = request.POST.get('methode')
        motif = request.POST.get('motif')
        notes = request.POST.get('notes', '')

        try:
            eleve = Eleve.objects.get(id=eleve_id)
            ComptaService.enregistrer_paiement_manuel(
                eleve=eleve,
                montant=montant,
                methode=methode,
                motif=motif,
                user=request.user,
                notes=notes
            )
            messages.success(request, "Paiement manuel enregistré avec succès. Il est en attente de validation.")
            return redirect('finance:transactions')
        except Eleve.DoesNotExist:
            messages.error(request, "Élève introuvable.")

    eleves = Eleve.objects.filter(statut=Eleve.Statut.ACTIF)
    return render(request, 'pages/finance/paiement_manuel.html', {'eleves': eleves})

@login_required
@finance_required
def valider_transaction(request, id):
    try:
        ComptaService.valider_paiement(transaction_id=id, admin_user=request.user)
        messages.success(request, f"La transaction #{id} a été validée.")
    except Exception as e:
        messages.error(request, f"Erreur de validation: {str(e)}")
        
    return redirect('finance:transactions')
