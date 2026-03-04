from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid

class Cycle(models.Model):
    """Maternelle, Primaire, Collège, Lycée"""
    nom = models.CharField(max_length=50, unique=True, verbose_name=_("Nom du cycle"))
    ordre = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.nom

class NiveauScolaire(models.Model):
    """1ère année, 7ème année, Terminale, etc."""
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='niveaux')
    nom = models.CharField(max_length=50, verbose_name=_("Nom du niveau"))
    ordre = models.PositiveSmallIntegerField(default=1)
    est_annee_examen = models.BooleanField(default=False, help_text="CEE, BEPC, BAC")
    label_examen = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['cycle__ordre', 'ordre']
        unique_together = ('cycle', 'nom')

    def __str__(self):
        return f"{self.nom} ({self.cycle.nom})"

class Classe(models.Model):
    BRANCHE_CHOICES = [
        ('SM', 'Sciences Mathématiques'),
        ('SS', 'Sciences Sociales'),
        ('SE', 'Sciences Expérimentales'),
        ('GEN', 'Général'),
    ]
    
    nom = models.CharField(max_length=50, unique=True, verbose_name=_("Nom de la classe"))
    niveau_scolaire = models.ForeignKey(NiveauScolaire, on_delete=models.PROTECT, related_name='classes', null=True)
    branche = models.CharField(max_length=20, choices=BRANCHE_CHOICES, default='GEN')
    annee_scolaire = models.CharField(max_length=9, default='2023-2024')
    frais_mensuel_attendu = models.DecimalField(max_digits=10, decimal_places=0, default=0, help_text="Montant en GNF")

    def __str__(self):
        return f"{self.nom} - {self.niveau_scolaire.nom if self.niveau_scolaire else ''}"

class Eleve(models.Model):
    class Statut(models.TextChoices):
        ACTIF = 'ACTIF', _('Actif')
        INACTIF = 'INACTIF', _('Inactif')
        RENVOYE = 'RENVOYE', _('Renvoyé')

    class Sexe(models.TextChoices):
        MASCULIN = 'M', _('Masculin')
        FEMININ = 'F', _('Féminin')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='profil_eleve'
    )
    matricule = models.CharField(max_length=20, unique=True, db_index=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=Sexe.choices)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.PROTECT, related_name='eleves')
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.ACTIF)
    photo = models.ImageField(upload_to='eleves_photos/', null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.matricule} - {self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Parent(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profil_parent'
    )
    nom_complet = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20, unique=True)
    adresse = models.TextField(blank=True)
    profession = models.CharField(max_length=100, blank=True)
    enfants = models.ManyToManyField(Eleve, related_name='parents', blank=True)

    def __str__(self):
        return f"{self.nom_complet} ({self.telephone})"
