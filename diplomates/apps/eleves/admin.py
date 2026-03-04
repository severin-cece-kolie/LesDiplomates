from django.contrib import admin
from .models import Classe, Eleve, Parent, Cycle, NiveauScolaire

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre')

@admin.register(NiveauScolaire)
class NiveauScolaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'cycle', 'ordre', 'est_annee_examen')
    list_filter = ('cycle',)

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau_scolaire', 'branche', 'annee_scolaire', 'frais_mensuel_attendu')
    list_filter = ('niveau_scolaire__cycle', 'niveau_scolaire', 'annee_scolaire', 'branche')

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'prenom', 'nom', 'classe', 'statut')
    list_filter = ('classe', 'statut', 'sexe')
    search_fields = ('matricule', 'nom', 'prenom')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'telephone')
    search_fields = ('nom_complet', 'telephone')
    filter_horizontal = ('enfants',)
