import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomates.settings')
django.setup()

from apps.eleves.models import Cycle, NiveauScolaire

def init_guinean_system():
    # Cycles et Niveaux
    cycles = [
        ('Maternelle', 1, [('Petite Section', 1), ('Moyenne Section', 2), ('Grande Section', 3)]),
        ('Primaire', 2, [('1ère année', 1), ('2ème année', 2), ('3ème année', 3), ('4ème année', 4), ('5ème année', 5), ('6ème année', 6, True, 'CEE')]),
        ('Collège', 3, [('7ème année', 1), ('8ème année', 2), ('9ème année', 3), ('10ème année', 4, True, 'BEPC')]),
        ('Lycée', 4, [('11ème année', 1), ('12ème année', 2), ('Terminale', 3, True, 'BAC')]),
    ]

    for cycle_nom, cycle_ordre, niveaux in cycles:
        cycle_obj, _ = Cycle.objects.get_or_create(nom=cycle_nom, defaults={'ordre': cycle_ordre})
        for niv_data in niveaux:
            nom_niv = niv_data[0]
            ordre_niv = niv_data[1]
            est_examen = niv_data[2] if len(niv_data) > 2 else False
            label_examen = niv_data[3] if len(niv_data) > 3 else None
            
            NiveauScolaire.objects.get_or_create(
                cycle=cycle_obj, 
                nom=nom_niv, 
                defaults={'ordre': ordre_niv, 'est_annee_examen': est_examen, 'label_examen': label_examen}
            )

    # Création des Classes spécifiques pour le Lycée avec Branches
    from apps.eleves.models import Classe
    lycee_cycle = Cycle.objects.get(nom='Lycée')
    branches = [('SM', 'Sciences Mathématiques'), ('SS', 'Sciences Sociales'), ('SE', 'Sciences Expérimentales')]
    annees = ['11ème année', '12ème année', 'Terminale']

    for annee in annees:
        niveau = NiveauScolaire.objects.get(cycle=lycee_cycle, nom=annee)
        for branche_code, branche_nom in branches:
            classe_nom = f"{annee} {branche_code}"
            Classe.objects.get_or_create(
                nom=classe_nom,
                defaults={
                    'niveau_scolaire': niveau,
                    'branche': branche_code,
                    'annee_scolaire': '2025-2026'
                }
            )
    print("Système éducatif guinéen et classes du Lycée initialisés.")

if __name__ == "__main__":
    init_guinean_system()
