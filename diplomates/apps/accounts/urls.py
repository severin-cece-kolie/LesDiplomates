from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.splash, name='splash'),
    path('connexion/', views.CustomLoginView.as_view(), name='login'),
    path('inscription/', views.register, name='register'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
