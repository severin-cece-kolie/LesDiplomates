from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.eleves.models import Eleve
from .models import Badge
import qrcode
from io import BytesIO
from django.core.files import File

@receiver(post_save, sender=Eleve)
def create_student_badge(sender, instance, created, **kwargs):
    """
    Crée automatiquement un Badge et génère l'image du QR Code
    lorsqu'un nouvel élève est ajouté au système.
    """
    if created:
        badge = Badge.objects.create(eleve=instance)
        
        # Génération du contenu du QR Code (l'UUID du badge)
        qr_data = str(badge.id)
        
        # Création de l'image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarde en mémoire puis dans le champ ImageField
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"badge_{instance.matricule}.png"
        
        badge.qr_code.save(file_name, File(buffer), save=True)
