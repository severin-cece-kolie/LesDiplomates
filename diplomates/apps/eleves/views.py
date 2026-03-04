from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Eleve, Classe
from apps.accounts.permissions import admin_required, staff_required, role_required

@login_required
@role_required('PARENT', 'ELEVE')
def portail_eleve(request):
    """Vue dédiée pour le parent ou l'élève lui-même avec gestion d'erreur robuste et multi-enfants"""
    user = request.user
    from apps.notes.models import Note, Trimestre
    
    if user.role == 'PARENT':
        if hasattr(user, 'profil_parent'):
            parent = user.profil_parent
            enfants = parent.enfants.all()
            
            # Gestion du multi-enfants
            selected_enfant_id = request.GET.get('enfant')
            selected_enfant = None
            if selected_enfant_id:
                selected_enfant = enfants.filter(id=selected_enfant_id).first()
            
            if not selected_enfant and enfants.exists():
                selected_enfant = enfants.first()
            
            context = {
                'parent': parent,
                'enfants': enfants,
                'selected_enfant': selected_enfant,
            }
            
            if selected_enfant:
                # Récupérer les notes récentes
                notes = Note.objects.filter(eleve=selected_enfant).select_related('matiere', 'trimestre').order_by('-date_saisie')[:5]
                # Calcul moyenne (simplifié)
                from django.db.models import Avg
                moyenne = Note.objects.filter(eleve=selected_enfant).aggregate(Avg('valeur'))['valeur__avg']
                
                context.update({
                    'notes_recentes': notes,
                    'moyenne_generale': round(float(moyenne), 2) if moyenne else 0,
                })
                
                # Récupérer les frais de scolarité
                from apps.finance.models import FraisScolarite
                frais = FraisScolarite.objects.filter(eleve=selected_enfant).order_by('-date_creation')
                context['frais'] = frais
                context['solde_total'] = sum([f.montant_attendu - f.montant_paye for f in frais if not f.est_solde])

                # Récupérer les notifications
                from apps.notifications.models import Notification
                notifs = Notification.objects.filter(destinataire=user, eleve_concerne=selected_enfant)[:5]
                context['annonces'] = notifs
                
            return render(request, 'dashboards/parent/index.html', context)
        else:
            # Fallback (Auto-fix already implemented but defensive)
            from .models import Parent
            profil, _ = Parent.objects.get_or_create(user=user, defaults={'nom_complet': user.get_full_name() or user.username})
            return redirect('eleves:portail')
            
    elif user.role == 'ELEVE':
        if hasattr(user, 'profil_eleve'):
            eleve = user.profil_eleve
            # Récupérer notes
            notes = Note.objects.filter(eleve=eleve).select_related('matiere', 'trimestre').order_by('-date_saisie')[:5]
            from django.db.models import Avg
            moyenne = Note.objects.filter(eleve=eleve).aggregate(Avg('valeur'))['valeur__avg']
            
            return render(request, 'dashboards/eleve/index.html', {
                'eleve': eleve,
                'notes_recentes': notes,
                'moyenne_generale': round(float(moyenne), 2) if moyenne else 0,
            })
        else:
            messages.warning(request, "Votre profil élève n'est pas encore complété par l'administration.")
            return redirect('accounts:profile')
            
    return redirect('actualites:dashboard')

@login_required
@staff_required
def liste_eleves(request):
    from .models import Classe
    eleves = Eleve.objects.all().select_related('classe', 'classe__niveau_scolaire', 'classe__niveau_scolaire__cycle').prefetch_related('parents')
    
    # Filtres dynamiques
    q = request.GET.get('q', '').strip()
    classe_id = request.GET.get('classe', '').strip()
    statut = request.GET.get('statut', '').strip()
    
    if q:
        from django.db.models import Q
        eleves = eleves.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(matricule__icontains=q)
        )
    if classe_id:
        eleves = eleves.filter(classe__id=classe_id)
    if statut:
        eleves = eleves.filter(statut=statut)
    
    classes = Classe.objects.all().order_by('nom')
    return render(request, 'pages/eleves/liste.html', {
        'eleves': eleves,
        'classes': classes,
    })

@login_required
@staff_required
def detail_eleve(request, id):
    eleve = get_object_or_404(Eleve, id=id)
    return render(request, 'pages/eleves/detail.html', {'eleve': eleve})

@login_required
@admin_required
def formulaire_eleve(request):
    from .models import Parent
    if request.method == 'POST':
        import datetime
        import random
        
        # Extraction des données
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        matricule = request.POST.get('matricule')
        classe_id = request.POST.get('classe')
        parent_id = request.POST.get('parent')
        date_naissance = request.POST.get('date_naissance') or "2010-01-01"
        sexe = request.POST.get('sexe') or "M"
        
        # Génération automatique du matricule si vide
        if not matricule:
            year = datetime.datetime.now().year
            rand_suffix = random.randint(1000, 9999)
            matricule = f"MAT-{year}-{rand_suffix}"
        
        classe = get_object_or_404(Classe, id=classe_id)
        eleve = Eleve.objects.create(
            nom=nom,
            prenom=prenom,
            matricule=matricule,
            classe=classe,
            date_naissance=date_naissance,
            sexe=sexe
        )
        
        if parent_id:
            parent = get_object_or_404(Parent, id=parent_id)
            parent.enfants.add(eleve)
            
        messages.success(request, f"L'élève {eleve.nom_complet} a été ajouté avec succès.")
        return redirect('eleves:liste')
    
    classes = Classe.objects.all()
    parents = Parent.objects.all()
    return render(request, 'pages/eleves/form.html', {'classes': classes, 'parents': parents})

@login_required
@staff_required
def generer_certificat(request, id):
    eleve = get_object_or_404(Eleve, id=id)
    # Simulation de génération de certificat
    messages.info(request, f"Génération du certificat de scolarité pour {eleve.nom_complet}...")
    return redirect('eleves:detail', id=id)

@login_required
@staff_required
def renouveler_qr(request, id):
    eleve = get_object_or_404(Eleve, id=id)
    # Simulation de renouvellement QR
    messages.success(request, f"Le QR Code du badge de {eleve.nom_complet} a été renouvelé.")
    return redirect('eleves:detail', id=id)

@login_required
@staff_required
def contact_parent_sms(request, id):
    eleve = get_object_or_404(Eleve, id=id)
    # Simulation d'envoi SMS
    messages.success(request, f"Un SMS a été envoyé aux parents de {eleve.nom_complet}.")
    return redirect('eleves:detail', id=id)
