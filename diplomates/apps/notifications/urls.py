from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('api/notifications/count/', views.notifications_count, name='notifications_count'),
]
