from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.eleves.models import Eleve, Classe
from apps.finance.models import Transaction
from apps.notifications.services import NotificationService
from apps.notifications.models import Notification, TemplateNotification

User = get_user_model()

class NotificationServiceTest(TestCase):
    
    def setUp(self):
        # Créer une classe
        self.classe = Classe.objects.create(
            nom='Test Classe',
            frais_mensuel_attendu=50000
        )
        
        # Créer un parent
        self.parent_user = User.objects.create_user(
            username='parent1',
            email='parent@test.com',
            password='test123'
        )
        
        # Créer un élève
        self.eleve = Eleve.objects.create(
            matricule='TEST001',
            nom='Test',
            prenom='Eleve',
            sexe='M',
            date_naissance='2010-01-01',
            classe=self.classe
        )
        
        # Associer le parent à l'élève
        from apps.eleves.models import Parent
        parent = Parent.objects.create(
            user=self.parent_user,
            nom_complet='Parent Test',
            telephone='624000000'
        )
        parent.enfants.add(self.eleve)
    
    def test_notification_inscription(self):
        """Test la notification après inscription d'élève"""
        # Créer les templates
        TemplateNotification.objects.create(
            type_notification='INSCRIPTION_ELEVE',
            sujet_email='Test sujet',
            template_email='Test message',
            template_sms='Test SMS',
            variables_disponibles='{nom_eleve}, {prenom_eleve}'
        )
        
        # Envoyer la notification
        result = NotificationService.envoyer_notification_inscription(self.eleve)
        
        # Vérifier que la notification a été créée
        self.assertTrue(result)
        notification = Notification.objects.filter(
            destinataire=self.parent_user,
            type_notification='INSCRIPTION_ELEVE'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.eleve_concerne, self.eleve)
        self.assertEqual(notification.statut, 'ENVOYE')
    
    def test_notification_paiement(self):
        """Test la notification après validation de paiement"""
        # Créer les templates
        TemplateNotification.objects.create(
            type_notification='PAIEMENT_VALIDATION',
            sujet_email='Paiement validé',
            template_email='Paiement message',
            template_sms='Paiement SMS',
            variables_disponibles='{nom_eleve}, {montant}'
        )
        
        # Créer une transaction validée
        transaction = Transaction.objects.create(
            eleve=self.eleve,
            montant=50000,
            methode='ORANGE',
            statut='VALIDE'
        )
        
        # Envoyer la notification
        result = NotificationService.envoyer_notification_paiement(transaction)
        
        # Vérifier que la notification a été créée
        self.assertTrue(result)
        notification = Notification.objects.filter(
            destinataire=self.parent_user,
            type_notification='PAIEMENT_VALIDATION'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.eleve_concerne, self.eleve)
        self.assertEqual(notification.statut, 'ENVOYE')
