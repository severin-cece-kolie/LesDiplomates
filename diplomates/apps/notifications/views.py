from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Notification

@login_required
def notifications_list(request):
    """Liste des notifications pour l'utilisateur connecté"""
    notifications = Notification.objects.filter(destinataire=request.user).order_by('-date_envoi')
    
    # Marquer comme lues les notifications non lues
    notifications_non_lues = notifications.filter(date_lu__isnull=True)
    notifications_non_lues.update(date_lu=timezone.now())
    
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def notifications_count(request):
    """API pour compter les notifications non lues"""
    count = Notification.objects.filter(destinataire=request.user, date_lu__isnull=True).count()
    return JsonResponse({'count': count})
