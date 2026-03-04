from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Transaction, FraisScolarite
from apps.eleves.models import Eleve
from apps.notifications.services import NotificationService

class ComptaService:
    """Service pour gérer la logique financière complexe de manière encapsulée"""
    
    @staticmethod
    @transaction.atomic
    def valider_paiement(transaction_id, admin_user):
        """
        Valide un paiement et met à jour les frais de scolarité associés de l'élève.
        Garantit via transaction.atomic que la DB reste cohérente en cas de plantage.
        """
        try:
            trans = Transaction.objects.get(id=transaction_id, statut='ATTENTE')
        except Transaction.DoesNotExist:
            raise ValidationError("Transaction introuvable ou déjà traitée.")
            
        trans.statut = 'VALIDE'
        trans.valide_par = admin_user
        trans.updated_at = timezone.now()
        trans.save()
        
        # Logique d'affectation : on prend les frais non soldés les plus anciens de l'élève
        montant_restant = trans.montant
        frais_impayes = FraisScolarite.objects.filter(
            eleve=trans.eleve, 
            est_solde=False
        ).order_by('date_creation')
        
        for frais in frais_impayes:
            if montant_restant <= 0:
                break
                
            reste_a_payer = frais.montant_attendu - frais.montant_paye
            
            if montant_restant >= reste_a_payer:
                frais.montant_paye += reste_a_payer
                frais.est_solde = True
                montant_restant -= reste_a_payer
            else:
                frais.montant_paye += montant_restant
                montant_restant = 0
                
            frais.save()
            
        # Déclencher la notification automatique
        NotificationService.envoyer_notification_paiement(trans)
        
        return trans

    @staticmethod
    def enregistrer_paiement_manuel(eleve, montant, methode, motif, user, notes=""):
        with transaction.atomic():
            # Créer la transaction
            transaction_obj = Transaction.objects.create(
                eleve=eleve,
                montant=montant,
                methode=methode,
                motif=motif,
                notes=notes,
                enregistre_par=user,
                statut='ATTENTE'
            )
            
            # Créer ou mettre à jour les frais de scolarité
            frais, created = FraisScolarite.objects.get_or_create(
                eleve=eleve,
                type_frais='MENSUALITE',
                mois_concerne=timezone.now().date().replace(day=1),
                defaults={
                    'montant_attendu': eleve.classe.frais_mensuel_attendu,
                    'montant_paye': montant,
                    'est_solde': montant >= eleve.classe.frais_mensuel_attendu
                }
            )
            
            if not created:
                frais.montant_paye += montant
                frais.est_solde = frais.montant_paye >= frais.montant_attendu
                frais.save()
            
            return transaction_obj
