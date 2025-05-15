from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('viagens/', views.listar_viagens, name='listagem_viagens_servidor'),
    path('cadastrar/', views.cadastrar_servidor, name='cadastrar_servidor'),
    path('listar-servidores/', views.listar_servidores, name='listar_servidores'),
    path('editar-servidor/<int:servidor_cpf>/', views.editar_servidor, name='editar_servidor'),
    path('excluir-servidor/<int:servidor_cpf>/', views.excluir_servidor, name='excluir_servidor'),
]