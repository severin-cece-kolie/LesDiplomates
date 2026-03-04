from django.db import models
from apps.eleves.models import Eleve
import uuid

class Badge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eleve = models.OneToOneField(Eleve, on_delete=models.CASCADE, related_name='badge')
    qr_code = models.ImageField(upload_to='badges/qrcodes/', blank=True)
    est_actif = models.BooleanField(default=True)
    date_emission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badge - {self.eleve.nom_complet} - {'Actif' if self.est_actif else 'Inactif'}"

class ScanLog(models.Model):
    RESULT_CHOICES = [
        ('OK', 'Accès Autorisé'),
        ('INVALIDE', 'Badge Invalide'),
        ('INACTIF', 'Badge Désactivé'),
        ('ECHEC_FINANCE', 'Bloqué (Scolarité)'),
    ]

    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='scans', null=True, blank=True)
    uuid_scanne = models.CharField(max_length=100, blank=True)  # Si le badge n'existe pas
    resultat = models.CharField(max_length=20, choices=RESULT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    agent = models.CharField(max_length=100, blank=True, help_text="Nom/ID de l'agent ou de la borne")

    def __str__(self):
        return f"Scan: {self.get_resultat_display()} le {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
