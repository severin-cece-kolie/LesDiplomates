from django.urls import path
from . import views

app_name = 'actualites'

urlpatterns = [
    path('', views.home, name='home'),
    path('accueil/', views.accueil, name='accueil'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('actualites/', views.actualites, name='actualites'),
    path('contact/', views.contact, name='contact'),
    path('programmes/', views.programmes, name='programmes'),
    path('cycles/', views.cycles, name='cycles'),
    path('vie-scolaire/', views.vie_scolaire, name='vie_scolaire'),
    path('a-propos/', views.about, name='about'),
    path('equipe/', views.equipe, name='equipe'),
    path('emplois/', views.emplois, name='emplois'),
    path('reglement/', views.reglement, name='reglement'),
    path('support/', views.support, name='support'),
    path('visite-virtuelle/', views.visite_virtuelle, name='visite_virtuelle'),
    path('confidentialite/', views.privacy, name='privacy'),
    path('conditions-utilisation/', views.terms, name='terms'),
]
