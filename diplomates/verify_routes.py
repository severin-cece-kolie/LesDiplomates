import os
import sys
import django

# Set up Django environment
sys.path.append('c:\\Users\\hp\\Desktop\\diplomates')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplomates.settings')
django.setup()

from django.urls import reverse, resolve
from django.test import Client

def verify_urls():
    test_urls = [
        ('home', {}),
        ('eleves_liste', {}),
        ('finance_dashboard', {}),
        ('notes_classes', {}),
        ('notes_saisie', {'id': 1}),  # Assuming 1 exists or just checking resolution
        ('login', {}),
    ]
    
    print("--- URL Resolution Verification ---")
    for name, kwargs in test_urls:
        try:
            url = reverse(name, kwargs=kwargs)
            print(f"[OK] {name} -> {url}")
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

if __name__ == "__main__":
    verify_urls()
