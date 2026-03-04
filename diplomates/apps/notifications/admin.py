from django.contrib import admin
from .models import Notification, TemplateNotification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'destinataire', 'type_notification', 'canal', 'statut', 'date_envoi']
    list_filter = ['type_notification', 'canal', 'statut', 'date_envoi']
    search_fields = ['titre', 'destinataire__username', 'eleve_concerne__nom', 'eleve_concerne__prenom']
    readonly_fields = ['id', 'date_envoi']
    ordering = ['-date_envoi']

@admin.register(TemplateNotification)
class TemplateNotificationAdmin(admin.ModelAdmin):
    list_display = ['type_notification', 'sujet_email', 'est_actif']
    list_filter = ['type_notification', 'est_actif']
    search_fields = ['type_notification', 'sujet_email']
