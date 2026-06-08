from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('/')

def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return auth_views.LoginView.as_view(
        template_name='registration/login.html'
    )(request)

urlpatterns = [
    path('', home, name='login'),
    
    path('logout/', custom_logout, name='logout'),
    
    path('dashboard/', include('tableau_bord.urls')),
    
    path('facturation/', include('facturation.urls')),
    
    path('erp-admin-secret/', admin.site.urls),
]