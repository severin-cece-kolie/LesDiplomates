import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomates.settings')
django.setup()

from apps.actualites.models import SuccessStat

def init_stats():
    stats = [
        ('Réussite au CEE', 98.8, 2025),
        ('Réussite au BEPC', 97.5, 2025),
        ('Réussite au BAC', 94.2, 2025),
        ('Taux d\'admission SM', 100, 2025),
    ]

    for label, value, year in stats:
        SuccessStat.objects.get_or_create(
            label=label,
            defaults={'value': value, 'year': str(year), 'is_active': True}
        )
    print("Statistiques de réussite initialisées.")

if __name__ == "__main__":
    init_stats()
