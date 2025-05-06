from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm

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

def login_usuario(request):
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
    return render(request, 'login/login.html', {'form': form})

@login_required
def logado():
    return redirect('raiz')
