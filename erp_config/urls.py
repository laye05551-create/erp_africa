from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Page de connexion principale
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    
    # Déconnexion
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    
    # Dashboard
    path('dashboard/', include('tableau_bord.urls')),
    
    # Facturation
    path('facturation/', include('facturation.urls')),
    
    # Admin caché
    path('erp-admin-secret/', admin.site.urls),
]