import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomates.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.eleves.models import Classe, Eleve, Parent
from apps.badges.models import Badge
from apps.finance.models import FraisScolarite
from django.utils import timezone
import datetime

def run_setup():
    print("Création des comptes administrateurs et rôles...")
    users_data = [
        {'username': 'admin', 'password': 'Admin@2024!', 'role': CustomUser.Role.ADMIN, 'is_superuser': True, 'is_staff': True},
        {'username': 'parent1', 'password': 'Parent@2024!', 'role': CustomUser.Role.PARENT, 'is_staff': False},
        {'username': 'prof1', 'password': 'Prof@2024!', 'role': CustomUser.Role.PROFESSEUR, 'is_staff': False},
        {'username': 'eleve1', 'password': 'Eleve@2024!', 'role': CustomUser.Role.ELEVE, 'first_name': 'Amadou', 'last_name': 'Diallo', 'is_staff': False},
        {'username': 'eleve2', 'password': 'Eleve@2024!', 'role': CustomUser.Role.ELEVE, 'first_name': 'Fatoumata', 'last_name': 'Bah', 'is_staff': False},
    ]

    for ud in users_data:
        if not CustomUser.objects.filter(username=ud['username']).exists():
            user = CustomUser.objects.create_user(
                username=ud['username'],
                password=ud['password'],
                role=ud['role'],
                is_superuser=ud.get('is_superuser', False),
                is_staff=ud.get('is_staff', False)
            )
            # Add first_name and last_name if provided
            if 'first_name' in ud:
                user.first_name = ud['first_name']
            if 'last_name' in ud:
                user.last_name = ud['last_name']
            user.save()
            print(f"Utilisateur {ud['username']} ({ud['role']}) créé.")

    print("Création des classes...")
    c1, _ = Classe.objects.get_or_create(nom="Terminale SM", niveau="LYCEE", frais_mensuel_attendu=1200000)
    c2, _ = Classe.objects.get_or_create(nom="12ème Année SE", niveau="LYCEE", frais_mensuel_attendu=850000)

    if not Eleve.objects.exists():
        print("Création des élèves et génération des badges...")
        e1 = Eleve.objects.create(
            matricule="DPL-23-0145", prenom="Amadou", nom="Diallo", sexe="M", 
            date_naissance=datetime.date(2006, 3, 14), classe=c1
        )
        e2 = Eleve.objects.create(
            matricule="DPL-23-0146", prenom="Fatoumata", nom="Bah", sexe="F", 
            date_naissance=datetime.date(2007, 8, 21), classe=c2
        )

        # Parents
        print("Configuration des parents...")
        parent_user = CustomUser.objects.get(username='parent1')
        p1, _ = Parent.objects.get_or_create(
            user=parent_user, nom_complet="Moussa Diallo", telephone="+224622112233"
        )
        p1.enfants.add(e1)
        
        print("Génération des frais de scolarité initiaux...")
        FraisScolarite.objects.create(eleve=e1, type_frais='MENSUALITE', montant_attendu=1200000)
        FraisScolarite.objects.create(eleve=e2, type_frais='MENSUALITE', montant_attendu=850000)
        
        print("Données de démonstration créées avec succès !")
    else:
        print("Les élèves existent déjà. Setup terminé.")

if __name__ == '__main__':
    run_setup()
