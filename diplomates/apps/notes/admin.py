from django.contrib import admin
from .models import Matiere, Trimestre, Note

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient')

@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee_scolaire', 'est_actif')
    list_filter = ('annee_scolaire', 'est_actif')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'valeur', 'trimestre', 'professeur')
    list_filter = ('trimestre', 'matiere', 'professeur')
    search_fields = ('eleve__nom', 'eleve__prenom')
