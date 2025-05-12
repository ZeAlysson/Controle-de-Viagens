from django.shortcuts import render

from autenticacao.forms import LoginServidoresForm
from controle.models import Controle
from servidor.models import Servidor

# Create your views here.
def listar_viagens(request):
    return render(request, 'global/templates/listagem_viagens.html')

def listar_viagens(request):
    cpf = request.session.get("servidor_cpf")
    
    if not cpf:
        return _retornar_erro_login("CPF inválido ou sessão expirada. Faça login novamente.")

    try:
        servidor = Servidor.objects.get(cpf=cpf)
    except Servidor.DoesNotExist:
        return _retornar_erro_login("CPF não encontrado. Verifique e tente novamente.")

    viagens = Controle.objects.filter(servidor=servidor)
    return render(request, 'global/templates/listagem_viagens.html', {'viagens': viagens})


    
def _retornar_erro_login(mensagem):
    form = LoginServidoresForm()
    form.add_error('cpf', mensagem)
    return render(None, 'login/login.html', {'form': form})