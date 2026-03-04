import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomates.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.eleves.models import Parent

def fix():
    parents = CustomUser.objects.filter(role='PARENT')
    for p in parents:
        if not hasattr(p, 'profil_parent'):
            Parent.objects.create(
                user=p,
                nom_complet=p.get_full_name() or p.username,
                telephone=p.telephone or f"00000000_{p.id}"
            )
            print(f"Created profile for {p.username}")

if __name__ == "__main__":
    fix()
