from django.contrib import admin
from .models import Badge, ScanLog

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'eleve', 'est_actif', 'date_emission')
    list_filter = ('est_actif', 'date_emission')
    search_fields = ('eleve__nom', 'eleve__prenom', 'id')

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ('badge', 'resultat', 'agent', 'timestamp')
    list_filter = ('resultat', 'timestamp')
