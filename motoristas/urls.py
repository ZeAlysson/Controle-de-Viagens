from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_motorista, name='cadastrar_motorista'),
    path('listar-motoristas/', views.listar_motoristas, name='listar_motoristas'),
    path('excluir-motorista/<int:motorista_id>/', views.excluir_motorista, name='excluir_motorista'),
    path('editar-motorista/<int:motorista_id>/', views.editar_motorista, name='editar_motorista'),

    path('motorista/', views.listar_viagens, name='listagem_viagens_motorista'),

]