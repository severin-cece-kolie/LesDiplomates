from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from apps.eleves.models import Parent, Eleve, Classe

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.Role.PARENT:
            Parent.objects.get_or_create(
                user=instance,
                defaults={'nom_complet': instance.get_full_name() or instance.username, 'telephone': instance.telephone or instance.username}
            )
        elif instance.role == CustomUser.Role.ELEVE:
            # Note: Eleve requires a Classe and Date of Birth which might not be known here.
            # We create a shell or handle gracefully in the view.
            # For now, we only ensure Parent profiles are auto-created as that's the reported error.
            pass

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == CustomUser.Role.PARENT:
        if hasattr(instance, 'profil_parent'):
            instance.profil_parent.save()
