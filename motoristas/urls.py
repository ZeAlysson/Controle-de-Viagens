from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar/', cadastrar_motorista, name='cadastrar_motorista'),
    path('listar-motoristas/', listar_motoristas, name='listar_motoristas'),
    path('excluir-motorista/<int:motorista_id>/', excluir_motorista, name='excluir_motorista'),
    path('editar-motorista/<int:motorista_id>/', editar_motorista, name='editar_motorista'),


]