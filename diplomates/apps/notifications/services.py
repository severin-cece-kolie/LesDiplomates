from django.conf import settings
from django.template import Context, Template
from django.core.mail import send_mail
from django.utils import timezone
from .models import Notification, TemplateNotification
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    
    @staticmethod
    def envoyer_notification_inscription(eleve):
        """Envoyer une notification après inscription d'un élève"""
        try:
            # Récupérer les parents de l'élève
            parents = eleve.parents.all()
            
            # Créer le template de message
            template = TemplateNotification.objects.filter(
                type_notification='INSCRIPTION_ELEVE',
                est_actif=True
            ).first()
            
            if not template:
                # Template par défaut si non trouvé
                sujet = f"Inscription confirmée - {eleve.nom_complet}"
                message_email = f"""
Cher parent,

Nous vous informons que l'inscription de votre enfant {eleve.nom_complet} 
a été confirmée au Complexe Scolaire Les Diplomates.

Détails de l'inscription:
• Matricule: {eleve.matricule}
• Classe: {eleve.classe.nom}
• Date d'inscription: {eleve.date_inscription.strftime('%d/%m/%Y')}

Veuillez vous connecter au portail pour suivre la progression de votre enfant.

Cordialement,
L'équipe des Diplomates
"""
                message_sms = f"Inscription confirmee de {eleve.nom_complet} aux Diplomates. Matricule: {eleve.matricule}"
            else:
                sujet = template.render_template_email({'nom_eleve': eleve.nom, 'prenom_eleve': eleve.prenom, 'matricule': eleve.matricule, 'classe': eleve.classe.nom, 'date': eleve.date_inscription.strftime('%d/%m/%Y')})
                message_email = template.template_email.format(
                    nom_eleve=eleve.nom,
                    prenom_eleve=eleve.prenom,
                    matricule=eleve.matricule,
                    classe=eleve.classe.nom,
                    date=eleve.date_inscription.strftime('%d/%m/%Y')
                )
                message_sms = template.template_sms.format(
                    nom_eleve=eleve.nom,
                    prenom_eleve=eleve.prenom,
                    matricule=eleve.matricule
                )
            
            # Envoyer aux parents
            for parent in parents:
                # Notification système
                Notification.objects.create(
                    destinataire=parent.user,
                    eleve_concerne=eleve,
                    type_notification='INSCRIPTION_ELEVE',
                    canal='SYSTEM',
                    titre=sujet,
                    message=message_email,
                    statut='ENVOYE'
                )
                
                # Email
                if parent.user.email:
                    try:
                        send_mail(
                            sujet,
                            message_email,
                            settings.DEFAULT_FROM_EMAIL,
                            [parent.user.email],
                            fail_silently=False,
                        )
                        logger.info(f"Email d'inscription envoyé à {parent.user.email}")
                    except Exception as e:
                        logger.error(f"Erreur email inscription: {e}")
                
                # SMS (simulation - à intégrer avec un service SMS réel)
                NotificationService._envoyer_sms(parent.telephone, message_sms)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur notification inscription: {e}")
            return False
    
    @staticmethod
    def envoyer_notification_paiement(transaction):
        """Envoyer une notification après validation de paiement"""
        try:
            eleve = transaction.eleve
            parents = eleve.parents.all()
            
            template = TemplateNotification.objects.filter(
                type_notification='PAIEMENT_VALIDATION',
                est_actif=True
            ).first()
            
            if not template:
                sujet = f"Paiement validé - {transaction.ref}"
                message_email = f"""
Cher parent,

Nous vous confirmons la validation du paiement suivant:

• Référence: {transaction.ref}
• Élève: {eleve.nom_complet}
• Montant: {transaction.montant:,} GNF
• Méthode: {transaction.get_methode_display()}
• Date: {transaction.created_at.strftime('%d/%m/%Y à %H:%M')}

Le paiement a été appliqué au compte de votre enfant.

Merci pour votre confiance.

Cordialement,
L'équipe des Diplomates
"""
                message_sms = f"Paiement valide de {transaction.montant:,} GNF pour {eleve.nom_complet}. Ref: {transaction.ref}"
            else:
                sujet = template.sujet_email.format(
                    nom_eleve=eleve.nom,
                    montant=transaction.montant,
                    reference=transaction.ref
                )
                message_email = template.template_email.format(
                    nom_eleve=eleve.nom,
                    prenom_eleve=eleve.prenom,
                    montant=transaction.montant,
                    reference=transaction.ref,
                    date=transaction.created_at.strftime('%d/%m/%Y à %H:%M')
                )
                message_sms = template.template_sms.format(
                    nom_eleve=eleve.nom,
                    montant=transaction.montant,
                    reference=transaction.ref
                )
            
            # Envoyer aux parents
            for parent in parents:
                # Notification système
                Notification.objects.create(
                    destinataire=parent.user,
                    eleve_concerne=eleve,
                    type_notification='PAIEMENT_VALIDATION',
                    canal='SYSTEM',
                    titre=sujet,
                    message=message_email,
                    statut='ENVOYE'
                )
                
                # Email
                if parent.user.email:
                    try:
                        send_mail(
                            sujet,
                            message_email,
                            settings.DEFAULT_FROM_EMAIL,
                            [parent.user.email],
                            fail_silently=False,
                        )
                        logger.info(f"Email de paiement envoyé à {parent.user.email}")
                    except Exception as e:
                        logger.error(f"Erreur email paiement: {e}")
                
                # SMS
                NotificationService._envoyer_sms(parent.telephone, message_sms)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur notification paiement: {e}")
            return False
    
    @staticmethod
    def envoyer_rappel_paiement(eleve, montant_du):
        """Envoyer un rappel de paiement"""
        try:
            parents = eleve.parents.all()
            
            sujet = f"Rappel de paiement - {eleve.nom_complet}"
            message_email = f"""
Cher parent,

Nous vous rappelons qu'un paiement est en attente pour votre enfant {eleve.nom_complet}:

• Élève: {eleve.nom_complet} ({eleve.matricule})
• Classe: {eleve.classe.nom}
• Montant dû: {montant_du:,} GNF

Merci de régulariser la situation dès que possible.

Vous pouvez effectuer le paiement via le portail en ligne.

Cordialement,
L'équipe des Diplomates
"""
            message_sms = f"Rappel: Paiement en attente de {montant_du:,} GNF pour {eleve.nom_complet}. Merci de regulariser."
            
            for parent in parents:
                Notification.objects.create(
                    destinataire=parent.user,
                    eleve_concerne=eleve,
                    type_notification='RAPPEL_PAIEMENT',
                    canal='SYSTEM',
                    titre=sujet,
                    message=message_email,
                    statut='ENVOYE'
                )
                
                if parent.user.email:
                    try:
                        send_mail(
                            sujet,
                            message_email,
                            settings.DEFAULT_FROM_EMAIL,
                            [parent.user.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        logger.error(f"Erreur email rappel: {e}")
                
                NotificationService._envoyer_sms(parent.telephone, message_sms)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur notification rappel: {e}")
            return False
    
    @staticmethod
    def _envoyer_sms(telephone, message):
        """Service d'envoi SMS (à implémenter avec un vrai service)"""
        try:
            # Simulation - à remplacer avec un vrai service SMS
            logger.info(f"SMS envoyé à {telephone}: {message}")
            
            # Exemple d'intégration avec un service SMS:
            # import africastalking
            # at = africastalking.SMS(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
            # response = at.send(message, [telephone])
            
            return True
        except Exception as e:
            logger.error(f"Erreur envoi SMS: {e}")
            return False
