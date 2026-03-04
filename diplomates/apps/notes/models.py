from django.db import models
from django.conf import settings
from apps.eleves.models import Eleve, Classe

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    coefficient = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.nom} (Coef: {self.coefficient})"

class Trimestre(models.Model):
    nom = models.CharField(max_length=50) # ex: "1er Trimestre"
    annee_scolaire = models.CharField(max_length=9, default='2023-2024')
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} - {self.annee_scolaire}"

class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.PROTECT, related_name='notes')
    trimestre = models.ForeignKey(Trimestre, on_delete=models.PROTECT, related_name='notes')
    professeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'PROF'})
    
    valeur = models.DecimalField(max_digits=4, decimal_places=2, help_text="Note sur 20")
    appreciation = models.CharField(max_length=255, blank=True)
    date_saisie = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Évite d'avoir plusieurs notes pour le même trimestre/matiere
        unique_together = ('eleve', 'matiere', 'trimestre')

    def __str__(self):
        return f"{self.valeur}/20 - {self.eleve.nom_complet} ({self.matiere.nom})"
