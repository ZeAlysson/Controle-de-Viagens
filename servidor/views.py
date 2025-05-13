from django.shortcuts import redirect, render

from autenticacao.forms import LoginServidoresForm
from controle.models import Controle
from servidor.models import Servidor
from django.contrib import messages

# Create your views here.
def listar_viagens(request):
    return render(request, 'global/templates/listagem_viagens.html')

def listar_viagens(request):
    cpf = request.session.get("servidor_cpf")
    
    if not cpf:
        messages.error(request, "CPF inválido ou sessão expirada. Faça login novamente.")
        return redirect('login')
    
    try:
        servidor = Servidor.objects.get(cpf=cpf)
    except Servidor.DoesNotExist:
        messages.error(request, "CPF não encontrado. Verifique e tente novamente.")
        return redirect('login')
    
    viagens = Controle.objects.filter(servidor=servidor)
    return render(request, 'global/templates/listagem_viagens.html', {'viagens': viagens})