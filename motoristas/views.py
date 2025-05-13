from django.shortcuts import render, redirect, get_object_or_404
from controle.models import Controle
from .forms import MotoristaForm
from .models import Motorista
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def cadastrar_motorista(request):
    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_motoristas')
    else:
        form = MotoristaForm()

    return render(request, 'motoristas/cadastrar_motorista.html', {'form': form})

@login_required
def listar_motoristas(request):
    motoristas = Motorista.objects.all()
    return render(request, 'motoristas/listar_motoristas.html', {'motoristas': motoristas})

@login_required
def excluir_motorista(request, motorista_id):
    motorista = get_object_or_404(Motorista, pk=motorista_id)
    motorista.delete()
    return redirect('listar_motoristas')

@login_required
def editar_motorista(request, motorista_id):
    motorista = get_object_or_404(Motorista, pk=motorista_id)

    if request.method == 'POST':
        form = MotoristaForm(request.POST, instance=motorista)
        if form.is_valid():
            form.save()
            return redirect('listar_motoristas')
    else:
        form = MotoristaForm(instance=motorista)
    return render(request, 'motoristas/editar_motorista.html', {'form': form, 'motorista': motorista})

def listar_viagens(request):
    cpf = request.session.get("motorista_cpf")
    
    if not cpf:
        messages.error(request, "CPF inválido ou sessão expirada. Faça login novamente.")
        return redirect('login')
    
    try:
        motorista = Motorista.objects.get(cpf=cpf)
    except Motorista.DoesNotExist:
        messages.error(request, "CPF não encontrado. Verifique e tente novamente.")
        return redirect('login')
    
    viagens = Controle.objects.filter(motorista=motorista)
    return render(request, 'global/templates/listagem_viagens.html', {'viagens': viagens})

    