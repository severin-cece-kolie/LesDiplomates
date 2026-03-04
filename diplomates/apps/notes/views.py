from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg, Max
from apps.eleves.models import Classe, Eleve
from .models import Trimestre, Note, Matiere
from apps.accounts.permissions import admin_required, professeur_required, academique_required

@login_required
@academique_required
def liste_classes(request):
    classes = Classe.objects.all()
    return render(request, 'dashboards/prof/index.html', {'classes': classes})

@login_required
@academique_required
def saisie_notes(request, id):
    classe = get_object_or_404(Classe, id=id)
    matieres = Matiere.objects.all()
    trimestres = [
        (t.id, t.nom) for t in Trimestre.objects.filter(est_actif=True)
    ]
    
    selected_matiere_id = request.GET.get('matiere')
    selected_trimestre_id = request.GET.get('trimestre')
    
    matiere = None
    trimestre = None
    notes_existantes = {}
    eleves = Eleve.objects.filter(classe=classe)
    
    if selected_matiere_id and selected_trimestre_id:
        matiere = get_object_or_404(Matiere, id=selected_matiere_id)
        trimestre = get_object_or_404(Trimestre, id=selected_trimestre_id)
        
        if request.method == 'POST':
            action = request.POST.get('action')
            for eleve in eleves:
                valeur = request.POST.get(f'note_{eleve.pk}')
                commentaire = request.POST.get(f'commentaire_{eleve.pk}')
                
                if valeur:
                    note, created = Note.objects.update_or_create(
                        eleve=eleve,
                        matiere=matiere,
                        trimestre=trimestre,
                        defaults={
                            'valeur': valeur,
                            'appreciation': commentaire,
                            'professeur': request.user
                        }
                    )
            
            messages.success(request, "Les notes ont été enregistrées avec succès.")
            return redirect(f"{request.path}?matiere={selected_matiere_id}&trimestre={selected_trimestre_id}")

        # Fetch existing notes
        notes = Note.objects.filter(eleve__in=eleves, matiere=matiere, trimestre=trimestre)
        notes_existantes = {n.eleve_id: n for n in notes}

    # KPIs
    moyenne_classe = None
    note_max_obj = None
    nb_en_attente = eleves.count() - len(notes_existantes)
    
    if notes_existantes:
        notes_list = [n.valeur for n in notes_existantes.values()]
        moyenne_classe = sum(notes_list) / len(notes_list) if notes_list else 0
        note_max = max(notes_list) if notes_list else 0
        note_max_obj = next((n for n in notes_existantes.values() if n.valeur == note_max), None)

    return render(request, 'pages/notes/saisie.html', {
        'classe': classe,
        'matieres': matieres,
        'trimestres': trimestres,
        'matiere': matiere,
        'trimestre': selected_trimestre_id,
        'eleves': eleves,
        'notes_existantes': notes_existantes,
        'moyenne_classe': round(moyenne_classe, 2) if moyenne_classe is not None else None,
        'note_max_obj': note_max_obj,
        'nb_en_attente': nb_en_attente
    })

@login_required
def generer_bulletin(request, eleve_id, trimestre_id):
    eleve = get_object_or_404(Eleve, id=eleve_id)
    trimestre = get_object_or_404(Trimestre, id=trimestre_id)

    user = request.user
    if hasattr(user, 'is_parent') and user.is_parent() and hasattr(user, 'profil_parent'):
        if eleve not in user.profil_parent.enfants.all():
            return render(request, '403.html', status=403)
    if hasattr(user, 'is_eleve') and user.is_eleve():
        if eleve.user != user:
            return render(request, '403.html', status=403)

    notes = Note.objects.filter(eleve=eleve, trimestre=trimestre).select_related('matiere', 'professeur')

    # Calculs bulletin
    total_points = sum(float(n.valeur) * n.matiere.coefficient for n in notes)
    total_coef = sum(n.matiere.coefficient for n in notes)
    moyenne = round(total_points / total_coef, 2) if total_coef > 0 else 0

    # Classe moyenne (tous les élèves de la même classe)
    class_notes = Note.objects.filter(
        trimestre=trimestre, eleve__classe=eleve.classe
    )
    from django.db.models import Avg
    class_eleves = eleve.classe.eleves.all() if eleve.classe else []
    nb_eleves = len(class_eleves)

    # Rang : compter combien d'élèves ont une meilleure moyenne
    rang = 1
    for autre_eleve in class_eleves:
        if autre_eleve.id == eleve.id:
            continue
        notes_autre = Note.objects.filter(eleve=autre_eleve, trimestre=trimestre)
        tp = sum(float(n.valeur) * n.matiere.coefficient for n in notes_autre)
        tc = sum(n.matiere.coefficient for n in notes_autre)
        moy_autre = tp / tc if tc > 0 else 0
        if moy_autre > moyenne:
            rang += 1

    return render(request, 'pages/notes/bulletin.html', {
        'eleve': eleve,
        'trimestre': trimestre,
        'notes': notes,
        'total_points': round(total_points, 2),
        'total_coef': total_coef,
        'moyenne': moyenne,
        'rang': rang,
        'nb_eleves': nb_eleves,
    })
