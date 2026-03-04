from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('classes/', views.liste_classes, name='liste_classes'),
    path('saisie/<int:id>/', views.saisie_notes, name='saisie'),
    path('bulletin/<int:eleve_id>/<int:trimestre_id>/', views.generer_bulletin, name='bulletin'),
]
