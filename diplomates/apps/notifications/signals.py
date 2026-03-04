from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.eleves.models import Eleve
from apps.finance.models import Transaction
from .services import NotificationService

@receiver(post_save, sender=Eleve)
def notification_inscription_eleve(sender, instance, created, **kwargs):
    """Déclencher une notification après inscription d'un élève"""
    if created:
        # Envoyer la notification d'inscription
        NotificationService.envoyer_notification_inscription(instance)

@receiver(post_save, sender=Transaction)
def notification_paiement(sender, instance, created, **kwargs):
    """Déclencher une notification après validation de paiement"""
    # Vérifier si le statut passe à VALIDÉ
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.statut != 'VALIDE' and instance.statut == 'VALIDE':
            # Le paiement vient d'être validé
            NotificationService.envoyer_notification_paiement(instance)
    except sender.DoesNotExist:
        # Nouvelle transaction, ne pas envoyer de notification
        pass
