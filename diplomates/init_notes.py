import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomates.settings')
django.setup()

from apps.notes.models import Trimestre

def init_trimestres():
    trimestres = [
        {"nom": "1er Trimestre", "annee_scolaire": "2023-2024", "est_actif": True},
        {"nom": "2ème Trimestre", "annee_scolaire": "2023-2024", "est_actif": True},
        {"nom": "3ème Trimestre", "annee_scolaire": "2023-2024", "est_actif": True},
    ]
    
    for t_data in trimestres:
        t, created = Trimestre.objects.get_or_create(
            nom=t_data["nom"], 
            annee_scolaire=t_data["annee_scolaire"],
            defaults={"est_actif": t_data["est_actif"]}
        )
        if created:
            print(f"Créé : {t}")
        else:
            print(f"Existe déjà : {t}")

if __name__ == "__main__":
    init_trimestres()
