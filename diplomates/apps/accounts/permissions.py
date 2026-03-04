from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

# Mixins for Class-Based Views
class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

class IsFinanceMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_finance()

class IsProfesseurMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_professeur()

class IsParentMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_parent()

class IsEleveMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_eleve()

# Decorators for Function-Based Views
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_admin())(view_func)

def finance_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_finance())(view_func)

def professeur_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_professeur())(view_func)

def parent_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_parent())(view_func)

def eleve_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_eleve())(view_func)

def academique_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and (u.is_admin() or u.is_professeur()))(view_func)

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and (u.is_admin() or u.is_professeur() or u.is_finance()))(view_func)

def role_required(*roles):
    """
    Generic decorator for views that checks if the user has one of the required roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

from functools import wraps
from django.shortcuts import redirect
