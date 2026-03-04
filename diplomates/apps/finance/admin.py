from django.contrib import admin
from .models import Transaction, FraisScolarite

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('ref', 'eleve', 'montant', 'methode', 'statut', 'created_at')
    list_filter = ('statut', 'methode', 'created_at')
    search_fields = ('ref', 'eleve__nom', 'eleve__prenom')

@admin.register(FraisScolarite)
class FraisScolariteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'type_frais', 'montant_paye', 'montant_attendu', 'est_solde')
    list_filter = ('est_solde', 'type_frais')
