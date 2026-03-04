from django.db import models
from django.conf import settings
from apps.eleves.models import Eleve
import uuid

class FraisScolarite(models.Model):
    TYPE_CHOICES = [
        ('INSCRIPTION', 'Inscription'),
        ('MENSUALITE', 'Mensualité'),
        ('TRIMESTRE', 'Trimestre'),
        ('AUTRE', 'Autre Frais'),
    ]
    
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='frais_scolarite')
    type_frais = models.CharField(max_length=20, choices=TYPE_CHOICES, default='MENSUALITE')
    mois_concerne = models.DateField(null=True, blank=True, help_text="Premier jour du mois concerné")
    montant_attendu = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    est_solde = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_frais_display()} - {self.eleve.nom_complet} ({self.montant_paye}/{self.montant_attendu})"

class Transaction(models.Model):
    METHODE_CHOICES = [
        ('ESPECES', 'Espèces'),
        ('VIREMENT', 'Virement Bancaire'),
        ('MOMO', 'MTN MoMo'),
        ('ORANGE', 'Orange Money'),
    ]

    STATUT_CHOICES = [
        ('ATTENTE', 'En Attente'),
        ('VALIDE', 'Validé'),
        ('REJETE', 'Rejeté'),
    ]

    ref = models.CharField(max_length=50, unique=True, default=uuid.uuid4, db_index=True)
    eleve = models.ForeignKey(Eleve, on_delete=models.PROTECT, related_name='transactions')
    montant = models.DecimalField(max_digits=10, decimal_places=0)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='ATTENTE')
    
    enregistre_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, null=True, 
        related_name='transactions_enregistrees'
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='transactions_validees'
    )
    
    motif = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ref} - {self.montant} GNF - {self.get_statut_display()}"
