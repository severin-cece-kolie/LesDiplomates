from django.db import models
from django.utils.text import slugify

class RegulationChapter(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre du chapitre")
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(verbose_name="Contenu")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Chapitre du règlement"
        verbose_name_plural = "Chapitres du règlement"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class SuccessStat(models.Model):
    label = models.CharField(max_length=100, verbose_name="Libellé (ex: Réussite au CEE)")
    value = models.FloatField(verbose_name="Valeur (%)", help_text="Sera écrasé par le calcul automatique si un examen est lié")
    year = models.IntegerField(verbose_name="Année")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Statistique de réussite"
        verbose_name_plural = "Statistiques de réussite"

    def __str__(self):
        return f"{self.label} - {self.year}"

class TeamMember(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom complet")
    role = models.CharField(max_length=100, verbose_name="Poste / Fonction")
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Membre de l'équipe"

    def __str__(self):
        return self.name

class AdmissionExam(models.Model):
    EXAM_TYPES = [('CEE', 'CEE'), ('BEPC', 'BEPC'), ('BAC', 'BAC')]
    type = models.CharField(max_length=10, choices=EXAM_TYPES)
    annee = models.IntegerField()
    total_candidats = models.PositiveIntegerField()
    total_admis = models.PositiveIntegerField()

    @property
    def taux_reussite(self):
        if self.total_candidats > 0:
            return (self.total_admis / self.total_candidats) * 100
        return 0

    def __str__(self):
        return f"{self.type} {self.annee} - {self.taux_reussite:.1f}%"

class Actualite(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(max_length=500, help_text="Bref résumé")
    content = models.TextField()
    image = models.ImageField(upload_to='actualites/', null=True, blank=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_pub']
        verbose_name = "Actualité"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class SchoolLife(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='school_life/', null=True, blank=True)
    icon = models.CharField(max_length=50, help_text="Nom de l'icone Material Symbol", default="activity")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Vie Scolaire (Section)"
        verbose_name_plural = "Vie Scolaire (Sections)"

    def __str__(self):
        return self.title
