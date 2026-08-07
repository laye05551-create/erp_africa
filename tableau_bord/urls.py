from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ia/', views.analyse_ia, name='analyse_ia'),
]