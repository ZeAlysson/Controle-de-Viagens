from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('tela-principal/',tela_controle, name='tela_principal'),
    path('visualizar-controle/<int:controle_id>/', visualizar_controle, name='visualizar_controle'),
    path('editar-controle/<int:controle_id>/', editar_controle, name='editar_controle'),
    path('excluir-controle/<int:controle_id>/', excluir_controle, name='excluir_controle'),
    path('tela-controle/', tela_controle, name='tela_controle'),
    path('cadastrar-controle/', cadastrar_controle, name='cadastrar_controle'),

    # meus app
    path('veiculos/', include('veiculos.urls')),
    path('motoristas/', include('motoristas.urls')),


]