from django.urls import path
from . import views

app_name = 'eleves'

urlpatterns = [
    path('portail/', views.portail_eleve, name='portail'),
    path('liste/', views.liste_eleves, name='liste'),
    path('<int:id>/', views.detail_eleve, name='detail'),
    path('nouveau/', views.formulaire_eleve, name='nouveau'),
    path('<int:id>/certificat/', views.generer_certificat, name='certificat'),
    path('<int:id>/renouveler-qr/', views.renouveler_qr, name='renouveler_qr'),
    path('<int:id>/contact-sms/', views.contact_parent_sms, name='contact_sms'),
]
