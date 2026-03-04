from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrateur')
        FINANCE = 'FINANCE', _('Finance / Comptabilité')
        PROFESSEUR = 'PROF', _('Professeur')
        PARENT = 'PARENT', _('Parent')
        ELEVE = 'ELEVE', _('Élève')

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.ELEVE,
        verbose_name=_('Rôle utilisateur')
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Téléphone')
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_finance(self):
        return self.role == self.Role.FINANCE or self.is_admin()

    def is_professeur(self):
        return self.role == self.Role.PROFESSEUR

    def is_parent(self):
        return self.role == self.Role.PARENT

    def is_eleve(self):
        return self.role == self.Role.ELEVE
