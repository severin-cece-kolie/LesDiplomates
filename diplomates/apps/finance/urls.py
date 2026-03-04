from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.dashboard_finance, name='dashboard'),
    path('transactions/', views.liste_transactions, name='transactions'),
    path('transactions/<int:transaction_id>/validation/', views.transaction_validation, name='validation'),
    path('paiement/checkout/', views.payment_checkout, name='checkout'),
    path('paiement/confirmation/', views.payment_confirmation, name='confirmation'),
    path('paiement/manuel/', views.enregistrement_manuel, name='paiement_manuel'),
    path('transactions/<int:id>/valider/', views.valider_transaction, name='valider'),
]
