from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from motoristas.models import Motorista
from servidor.models import Servidor
from .forms import LoginServidoresForm, RegistroForm, LoginForm

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user != None:
                login(request=request, user=user)
                return redirect('logado')
    else:
        form = RegistroForm()
    return render(request, 'registro/registro.html', {'form': form})

def login_admin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request=request, user=user)
                return redirect('logado')
    else:
        form = LoginForm()
    return render(request, 'login/admin/login.html', {'form': form})

def login_servidores(request):
    if request.method == "POST":
        form = LoginServidoresForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            usuario = buscar_usuario_por_cpf(cpf)

            if usuario:
                # Armazena o CPF na sessão com base no tipo
                if isinstance(usuario, Servidor):
                    chave = 'servidor_cpf'
                    request.session[chave] = usuario.cpf
                    return redirect('listagem_viagens_servidor')
                else:
                    chave = 'motorista_cpf'
                    request.session[chave] = usuario.cpf
                    return redirect('listagem_viagens_motorista')
            
            form.add_error('cpf', "CPF não encontrado. Verifique e tente novamente.")
    else:
        form = LoginServidoresForm()

    return render(request, 'login/login.html', {'form': form})


@login_required
def logado(request):
    return redirect('raiz')


def buscar_usuario_por_cpf(cpf):
    for model in (Servidor, Motorista):
        try:
            return model.objects.get(cpf=cpf)
        except model.DoesNotExist:
            continue
    return None