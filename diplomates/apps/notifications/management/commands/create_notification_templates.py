from django.core.management.base import BaseCommand
from apps.notifications.models import TemplateNotification

class Command(BaseCommand):
    help = 'Créer les modèles de notifications par défaut'

    def handle(self, *args, **options):
        templates = [
            {
                'type_notification': 'INSCRIPTION_ELEVE',
                'sujet_email': 'Inscription confirmée - {prenom_eleve} {nom_eleve}',
                'template_email': '''Cher parent,

Nous vous informons que l'inscription de votre enfant {prenom_eleve} {nom_eleve} 
a été confirmée au Complexe Scolaire Les Diplomates.

Détails de l'inscription:
• Matricule: {matricule}
• Classe: {classe}
• Date d'inscription: {date}

Veuillez vous connecter au portail pour suivre la progression de votre enfant.

Cordialement,
L'équipe des Diplomates''',
                'template_sms': 'Inscription confirmee de {prenom_eleve} {nom_eleve} aux Diplomates. Matricule: {matricule}',
                'variables_disponibles': '{prenom_eleve}, {nom_eleve}, {matricule}, {classe}, {date}'
            },
            {
                'type_notification': 'PAIEMENT_VALIDATION',
                'sujet_email': 'Paiement validé - {reference}',
                'template_email': '''Cher parent,

Nous vous confirmons la validation du paiement suivant:

• Référence: {reference}
• Élève: {prenom_eleve} {nom_eleve}
• Montant: {montant:,} GNF
• Méthode: {methode}
• Date: {date}

Le paiement a été appliqué au compte de votre enfant.

Merci pour votre confiance.

Cordialement,
L'équipe des Diplomates''',
                'template_sms': 'Paiement valide de {montant:,} GNF pour {prenom_eleve} {nom_eleve}. Ref: {reference}',
                'variables_disponibles': '{prenom_eleve}, {nom_eleve}, {montant}, {reference}, {date}, {methode}'
            },
            {
                'type_notification': 'REJET_PAIEMENT',
                'sujet_email': 'Paiement rejeté - {reference}',
                'template_email': '''Cher parent,

Nous vous informons que le paiement suivant a été rejeté:

• Référence: {reference}
• Élève: {prenom_eleve} {nom_eleve}
• Montant: {montant:,} GNF
• Raison: {raison}

Veuillez contacter le service financier pour plus d'informations.

Cordialement,
L'équipe des Diplomates''',
                'template_sms': 'Paiement rejeté de {montant:,} GNF pour {prenom_eleve} {nom_eleve}. Ref: {reference}',
                'variables_disponibles': '{prenom_eleve}, {nom_eleve}, {montant}, {reference}, {raison}'
            },
            {
                'type_notification': 'RAPPEL_PAIEMENT',
                'sujet_email': 'Rappel de paiement - {prenom_eleve} {nom_eleve}',
                'template_email': '''Cher parent,

Nous vous rappelons qu'un paiement est en attente pour votre enfant {prenom_eleve} {nom_eleve}:

• Élève: {prenom_eleve} {nom_eleve} ({matricule})
• Classe: {classe}
• Montant dû: {montant:,} GNF

Merci de régulariser la situation dès que possible.

Vous pouvez effectuer le paiement via le portail en ligne.

Cordialement,
L'équipe des Diplomates''',
                'template_sms': 'Rappel: Paiement en attente de {montant:,} GNF pour {prenom_eleve} {nom_eleve}. Merci de regulariser.',
                'variables_disponibles': '{prenom_eleve}, {nom_eleve}, {matricule}, {classe}, {montant}'
            }
        ]

        for template_data in templates:
            template, created = TemplateNotification.objects.get_or_create(
                type_notification=template_data['type_notification'],
                defaults=template_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Template '{template_data['type_notification']}' créé avec succès")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Template '{template_data['type_notification']}' existe déjà")
                )
        
        self.stdout.write(
            self.style.SUCCESS('Création des templates de notifications terminée!')
        )
