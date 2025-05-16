from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from motoristas.models import Motorista
from .forms import LoginServidoresForm, RegistroForm, AdminLoginForm
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView


def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user != None:
                login(request=request, user=user)
                messages.success(request, f"Usuário {user.username} registrado com sucesso!")
                return redirect('login_admin')
    else:
        form = RegistroForm()
    return render(request, 'registro/registro.html', {'form': form})

def login_admin(request):
    if request.method == "POST":
        form = AdminLoginForm(request, data=request.POST) # Usar AdminLoginForm
        if form.is_valid():
            user = form.get_user() # Método correto para obter o usuário do AuthenticationForm
            if user is not None:
                if user.is_staff: # ESSENCIAL: Verificar se o usuário é staff/admin
                    login(request, user)
                    messages.success(request, f"Bem-vindo, Administrador {user.username}!")
                    return redirect('tela_principal')  # Ou sua URL de dashboard admin
                else:
                    messages.error(request, "Acesso negado. Esta conta não tem permissões de administrador.")
            else:
                # O formulário já trata "usuário ou senha inválidos" através de form.errors
                # mas pode-se adicionar uma mensagem genérica se preferir.
                messages.error(request, "Nome de usuário ou senha inválidos.")
        # else: # O formulário não é válido, os erros serão exibidos no template
        #     messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AdminLoginForm()
    return render(request, 'login/admin/login.html', {'form': form})

def login_servidores(request):
    if request.method == "POST":
        form = LoginServidoresForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            usuario = Motorista.objects.get(cpf=cpf)

            if usuario:
                chave = 'motorista_cpf'
                request.session[chave] = usuario.cpf
                return redirect('listagem_viagens_motorista')
            
        messages.error(request, "CPF inválido ou sessão expirada. Faça login novamente.")
        
    form = LoginServidoresForm()
    return render(request, 'login/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def logado(request):
    return redirect('raiz')


    
        
