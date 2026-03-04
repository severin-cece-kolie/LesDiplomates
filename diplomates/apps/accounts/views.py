from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_admin():
            return reverse('actualites:dashboard')
        elif user.is_finance():
            return reverse('finance:dashboard')
        elif user.is_professeur():
            return reverse('notes:liste_classes')
        elif user.is_parent() or user.is_eleve():
            return reverse('eleves:portail')
        return super().get_success_url()

def splash(request):
    """Page d'atterrissage intermédiaire avant la connexion"""
    if request.user.is_authenticated:
        return redirect('actualites:dashboard')
    return render(request, 'pages/splash.html')

from .forms import UserProfileForm
from apps.notes.models import Note
from apps.eleves.models import Eleve, Classe
from apps.finance.models import Transaction, FraisScolarite

@login_required
def profile(request):
    """User profile page - Different content based on role"""
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    
    # Get role-specific stats
    stats = {}
    if user.is_eleve():
        # Pour un élève, on pourrait compter ses badges (à implémenter si le modèle existe)
        stats['badges_count'] = 0 
        stats['notes_count'] = Note.objects.filter(eleve__user=user).count()
    elif user.is_parent():
        if hasattr(user, 'profil_parent'):
            stats['enfants_count'] = user.profil_parent.enfants.count()
        else:
            stats['enfants_count'] = 0
    elif user.is_professeur():
        stats['classes_count'] = Classe.objects.count() # À affiner si lien M2M existant
        stats['notes_saisies'] = Note.objects.filter(professeur=user).count()
    elif user.is_finance():
        stats['pending_payments'] = Transaction.objects.filter(statut='ATTENTE').count()
    elif user.is_admin():
        stats['users_count'] = CustomUser.objects.count()
    
    context = {
        'form': form,
        'user_role': user.get_role_display(),
        'is_admin': user.is_admin(),
        'is_finance': user.is_finance(),
        'is_professeur': user.is_professeur(),
        'is_parent': user.is_parent(),
        'is_eleve': user.is_eleve(),
        'stats': stats,
    }
    
    return render(request, 'accounts/profile.html', context)

def logout_view(request):
    """Vue de déconnexion avec message de confirmation"""
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        messages.success(request, f'Au revoir {user_name} ! Vous avez été déconnecté avec succès.')
    
    logout(request)
    return redirect('accounts:login')

def register(request):
    """Vue d'inscription pour les nouveaux utilisateurs"""
    if request.user.is_authenticated:
        return redirect('actualites:dashboard')
    
    if request.method == 'POST':
        form_data = request.POST
        
        # Validation basique des mots de passe
        if form_data.get('password1') != form_data.get('password2'):
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'registration/register.html')

        # Mapping des rôles (Frontend -> Backend)
        role_map = {
            'parent': CustomUser.Role.PARENT,
            'prof': CustomUser.Role.PROFESSEUR,
            'eleve': CustomUser.Role.ELEVE,
        }
        selected_role = role_map.get(form_data.get('role'), CustomUser.Role.ELEVE)

        try:
            # Créer l'utilisateur avec le rôle sélectionné
            user = CustomUser.objects.create_user(
                username=form_data['username'],
                email=form_data['email'],
                password=form_data['password1'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                role=selected_role
            )
            
            # Ajouter le téléphone
            user.telephone = form_data.get('telephone', '')
            user.save()
            
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('accounts:login')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création du compte: {str(e)}')
    
    return render(request, 'registration/register.html')
