from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('servidor/', views.listar_viagens, name='listagem_viagens_servidor'),
    
]