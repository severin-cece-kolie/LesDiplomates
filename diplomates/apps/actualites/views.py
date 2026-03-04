from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required
from .models import RegulationChapter, SuccessStat

def home(request):
    """Page d'accueil publique - Page de chargement animée"""
    return render(request, 'loading.html')

def accueil(request):
    """Vraie page d'accueil publique avec statistiques et cycles dynamiques"""
    from apps.eleves.models import Cycle
    from .models import SuccessStat, AdmissionExam
    
    # Récupération des stats manuelles actives
    stats = list(SuccessStat.objects.filter(is_active=True).order_by('-year')[:4])
    
    # On complète ou remplace par les données calculées des AdmissionExam
    exams = AdmissionExam.objects.all().order_by('-annee')
    for exam in exams:
        # On peut injecter dynamiquement dans la liste des stats
        exam_stat = {
            'label': f'Réussite au {exam.type}',
            'value': exam.taux_reussite,
            'year': exam.annee
        }
        # Si on a déjà une stat manuelle pour ce label/année, on peut décider de privilégier la calculée
        # Pour rester simple, on les ajoute à la liste si non présentes
        stats.append(exam_stat)

    cycles = Cycle.objects.all().prefetch_related('niveaux')
    return render(request, 'pages/home.html', {
        'stats': stats[:4],  # On garde les 4 plus pertinentes
        'cycles': cycles
    })

def actualites(request):
    """Page d'actualités publique - Dynamique"""
    from .models import Actualite
    news = Actualite.objects.filter(is_published=True)
    return render(request, 'pages/actualites.html', {'news': news})

def contact(request):
    """Page de contact publique"""
    return render(request, 'pages/contact.html')

def programmes(request):
    """Page des programmes (Cycles) — données dynamiques"""
    from apps.eleves.models import Cycle
    cycles = Cycle.objects.all().prefetch_related('niveaux__classes')
    return render(request, 'pages/programmes.html', {'cycles': cycles})

def cycles(request):
    """Page des cycles scolaires — données dynamiques"""
    from apps.eleves.models import Cycle
    cycles = Cycle.objects.all().prefetch_related('niveaux')
    return render(request, 'pages/cycles.html', {'cycles': cycles})

def vie_scolaire(request):
    """Page de la vie scolaire - Dynamique"""
    from .models import SchoolLife
    sections = SchoolLife.objects.all().order_by('order')
    return render(request, 'pages/vie_scolaire.html', {'sections': sections})

def about(request):
    """Page À propos"""
    return render(request, 'pages/about.html')

def equipe(request):
    """Page Notre équipe - Dynamique"""
    from .models import TeamMember
    members = TeamMember.objects.all().order_by('order')
    return render(request, 'pages/equipe.html', {'members': members})

def emplois(request):
    """Page Emplois"""
    return render(request, 'pages/emplois.html')

@login_required
@role_required('PARENT', 'PROF', 'ELEVE')
def reglement(request):
    """Page Règlement intérieur — Protégée (login requis)"""
    chapters = RegulationChapter.objects.all()
    return render(request, 'pages/reglement.html', {'chapters': chapters})

def support(request):
    """Page Support"""
    return render(request, 'pages/support.html')

def visite_virtuelle(request):
    """Page Visite Virtuelle avec galerie moderne"""
    return render(request, 'pages/visite_virtuelle.html')

def privacy(request):
    """Page Politique de Confidentialité"""
    return render(request, 'pages/privacy.html')

def terms(request):
    """Page Conditions d'Utilisation"""
    return render(request, 'pages/terms.html')

@login_required
def dashboard(request):
    """Redirige l'utilisateur vers son dashboard spécifique selon son rôle"""
    user = request.user
    
    if user.is_admin():
        from apps.finance.models import Transaction, FraisScolarite
        from apps.eleves.models import Eleve
        from apps.accounts.models import CustomUser
        from django.db.models import Sum
        
        # KPIs dynamiques pour le dashboard admin
        total_eleves = Eleve.objects.count()
        total_parents = CustomUser.objects.filter(role='PARENT').count()
        
        # Recettes du mois courant
        from django.utils import timezone
        now = timezone.now()
        recettes_mois = Transaction.objects.filter(
            statut='VALIDE',
            created_at__year=now.year,
            created_at__month=now.month
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        # Soldes impayés
        frais_impayes = FraisScolarite.objects.filter(est_solde=False)
        total_impaye = sum(f.montant_attendu - f.montant_paye for f in frais_impayes)
        nb_eleves_retard = frais_impayes.values('eleve').distinct().count()
        
        # Taux de recouvrement
        total_attendu = FraisScolarite.objects.aggregate(t=Sum('montant_attendu'))['t'] or 1
        total_paye = FraisScolarite.objects.aggregate(t=Sum('montant_paye'))['t'] or 0
        taux_recouvrement = round((total_paye / total_attendu) * 100) if total_attendu > 0 else 0
        
        # Transactions récentes
        recent_transactions = Transaction.objects.select_related('eleve').order_by('-created_at')[:5]
        
        # Répartition par méthode
        from django.db.models import Count
        methode_stats = Transaction.objects.filter(statut='VALIDE').values('methode').annotate(count=Count('id'), total=Sum('montant')).order_by('-total')
        methode_total = sum(m['count'] for m in methode_stats) or 1
        for m in methode_stats:
            m['pct'] = round((m['count'] / methode_total) * 100)
        
        # Journal d'activité : dernières transactions
        activites = Transaction.objects.select_related('eleve', 'enregistre_par').order_by('-created_at')[:5]
        
        return render(request, 'dashboards/admin/index.html', {
            'total_eleves': total_eleves,
            'total_parents': total_parents,
            'recettes_mois': recettes_mois,
            'total_impaye': total_impaye,
            'nb_eleves_retard': nb_eleves_retard,
            'taux_recouvrement': taux_recouvrement,
            'recent_transactions': recent_transactions,
            'methode_stats': methode_stats,
            'activites': activites,
            'mois_actuel': now.strftime('%B %Y'),
        })
    elif user.is_finance():
        return redirect('finance:dashboard')
    elif user.is_professeur():
        return redirect('notes:liste_classes')
    elif user.is_parent() or user.is_eleve():
        return redirect('eleves:portail')
    
    return redirect('actualites:dashboard')
