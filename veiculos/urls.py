from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar/', cadastrar_veiculo, name='cadastrar_veiculo'),
    path('listar-veiculo/', listar_veiculo, name='listar_veiculo'),
    path('excluir-veiculo/<int:veiculo_id>/', excluir_veiculo, name='excluir_veiculo'),
    path('editar-veiculo/<int:veiculo_id>/', editar_veiculo, name='editar_veiculo'),


]