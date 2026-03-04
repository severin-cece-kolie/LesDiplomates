from django.urls import path
from . import views

app_name = 'badges'

urlpatterns = [
    path('', views.liste_badges, name='liste'),
    path('verification/', views.verification_badge, name='verification'),
    path('student/<int:eleve_id>/', views.student_badge, name='student'),
    path('my-badge/', views.my_badge, name='my_badge'),
    path('generer-tous/', views.generer_tous_badges, name='generer_tous'),
    path('detail/<int:id>/', views.generer_badge_detail, name='detail'),
    path('api/scan/<uuid:badge_id>/', views.api_scan_badge, name='api_scan'),
]
