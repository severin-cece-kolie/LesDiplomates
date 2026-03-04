from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Badge, ScanLog
from apps.finance.models import FraisScolarite
from apps.eleves.models import Eleve
from apps.accounts.permissions import admin_required, eleve_required
import json

@login_required
@admin_required
def verification_badge(request):
    """Interface pour le personnel de sécurité avec scanner de QR Code"""
    return render(request, 'pages/badges/verification.html')

@login_required
def student_badge(request, eleve_id):
    """Afficher le badge d'un élève spécifique"""
    eleve = get_object_or_404(Eleve, id=eleve_id)
    
    # Vérifier si l'utilisateur a le droit de voir ce badge
    user = request.user
    if user.is_eleve() and user.eleve_profile != eleve:
        # Un élève ne peut voir que son propre badge
        return render(request, 'errors/403.html', status=403)
    
    return render(request, 'badges/student_badge.html', {'eleve': eleve})

@login_required
@eleve_required
def my_badge(request):
    """Afficher le badge de l'élève connecté"""
    try:
        eleve = request.user.eleve_profile
        return render(request, 'badges/student_badge.html', {'eleve': eleve})
    except AttributeError:
        return render(request, 'errors/404.html', status=404)

@login_required
@admin_required
def liste_badges(request):
    """Liste tous les élèves et l'état de leurs badges"""
    from apps.eleves.models import Classe
    badges = Badge.objects.all().select_related('eleve', 'eleve__classe')
    classes = Eleve.objects.values_list('classe__nom', 'classe__id').distinct()
    # Année scolaire dynamique
    annee = Classe.objects.values_list('annee_scolaire', flat=True).order_by('-annee_scolaire').first() or ''
    
    context = {
        'badges': badges,
        'total': badges.count(),
        'classes': [{'nom': c[0], 'pk': c[1]} for c in classes if c[0]],
        'annee': annee
    }
    return render(request, 'pages/badges/liste.html', context)

@login_required
@admin_required
def generer_tous_badges(request):
    """Génère les badges pour tous les élèves n'en ayant pas encore"""
    eleves_sans_badge = Eleve.objects.filter(badge__isnull=True)
    count = 0
    for eleve in eleves_sans_badge:
        Badge.objects.get_or_create(eleve=eleve)
        count += 1
    
    messages.success(request, f"{count} badges ont été générés avec succès.")
    return redirect('badges:liste')

@login_required
@admin_required
def generer_badge_detail(request, id):
    """Génère ou rafraîchit le badge d'un élève spécifique"""
    badge = get_object_or_404(Badge, pk=id)
    # Logique de génération de QR code ou autre ici
    messages.success(request, f"Badge de {badge.eleve.nom_complet} mis à jour.")
    return redirect('badges:liste')

@csrf_exempt
def api_scan_badge(request, badge_id):
    """API Endpoint pour le traitement d'un scan de badge"""
    if request.method == 'POST':
        try:
            badge = Badge.objects.select_related('eleve').get(id=badge_id)
            
            if not badge.est_actif:
                resultat = 'INACTIF'
                message = "Badge désactivé."
                success = False
            else:
                # Vérification financière (A-t-il des frais impayés en retard ?)
                impayes = FraisScolarite.objects.filter(
                    eleve=badge.eleve, 
                    est_solde=False
                )
                
                # Pour la règle métier : s'il doit plus de 0 GNF, il est bloqué (simplifié)
                montant_total_du = sum(f.montant_attendu - f.montant_paye for f in impayes)
                
                if montant_total_du > 0:
                    resultat = 'ECHEC_FINANCE'
                    message = f"Accès refusé. Impayés: {montant_total_du} GNF."
                    success = False
                else:
                    resultat = 'OK'
                    message = "Accès autorisé."
                    success = True
                    
            ScanLog.objects.create(
                badge=badge,
                resultat=resultat,
                agent=request.user.username if request.user.is_authenticated else "Scanner Auto"
            )
            
            return JsonResponse({
                'success': success,
                'message': message,
                'eleve': {
                    'nom': badge.eleve.nom_complet,
                    'matricule': badge.eleve.matricule,
                    'classe': badge.eleve.classe.nom,
                    'photo': badge.eleve.photo.url if badge.eleve.photo else None
                }
            })
            
        except Badge.DoesNotExist:
            ScanLog.objects.create(uuid_scanne=str(badge_id), resultat='INVALIDE')
            return JsonResponse({'success': False, 'message': 'Badge invalide ou inconnu.'}, status=404)
            
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
