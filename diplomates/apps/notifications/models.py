from django.db import models
from django.conf import settings
from apps.eleves.models import Eleve
import uuid

class Notification(models.Model):
    TYPE_CHOICES = [
        ('INSCRIPTION_ELEVE', 'Inscription Élève'),
        ('PAIEMENT_MENSUALITE', 'Paiement Mensualité'),
        ('PAIEMENT_VALIDATION', 'Validation Paiement'),
        ('REJET_PAIEMENT', 'Rejet Paiement'),
        ('RAPPEL_PAIEMENT', 'Rappel Paiement'),
        ('INFO_GENERALE', 'Information Générale'),
    ]
    
    CANAL_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('SYSTEM', 'System'),
    ]
    
    STATUT_CHOICES = [
        ('ENVOYE', 'Envoyé'),
        ('ERREUR', 'Erreur'),
        ('EN_ATTENTE', 'En Attente'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    eleve_concerne = models.ForeignKey(
        Eleve, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    type_notification = models.CharField(max_length=30, choices=TYPE_CHOICES)
    canal = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SYSTEM')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_lu = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.titre} - {self.destinataire.username}"
    
    class Meta:
        ordering = ['-date_envoi']

class TemplateNotification(models.Model):
    """Modèles de notifications prédéfinis"""
    TYPE_CHOICES = [
        ('INSCRIPTION_ELEVE', 'Inscription Élève'),
        ('PAIEMENT_MENSUALITE', 'Paiement Mensualité'),
        ('PAIEMENT_VALIDATION', 'Validation Paiement'),
        ('REJET_PAIEMENT', 'Rejet Paiement'),
        ('RAPPEL_PAIEMENT', 'Rappel Paiement'),
    ]
    
    type_notification = models.CharField(max_length=30, choices=TYPE_CHOICES, unique=True)
    sujet_email = models.CharField(max_length=200)
    template_email = models.TextField()
    template_sms = models.CharField(max_length=500)
    variables_disponibles = models.TextField(
        help_text="Variables disponibles: {nom_eleve}, {prenom_eleve}, {matricule}, {classe}, {montant}, {date}, {parent_nom}"
    )
    est_actif = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_type_notification_display()}"
