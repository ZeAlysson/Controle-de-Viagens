from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            print("entrei no form valid")
            user = form.save()
            login(request, user)
            return redirect('logado')
        else:
            print("erros: ", form.errors)
        
    else:
        form = RegistroForm()
    return render(request, 'registro/registro.html', {'form': form})

def login_usuario(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            login(request)
            return redirect('logado')
    else:
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

@login_required
def logado(request):
    return redirect('listar_veiculo')
