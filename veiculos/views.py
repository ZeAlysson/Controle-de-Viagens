from django.shortcuts import render, redirect, get_object_or_404
from .forms import VeiculoForm
from .models import Veiculo
from django.contrib.auth.decorators import login_required

@login_required
def cadastrar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_veiculo')
    else:
        form = VeiculoForm()

    return render(request, 'veiculos/cadastrar_veiculo.html', {'form': form})

@login_required
def listar_veiculo(request):
    veiculo = Veiculo.objects.all()
    return render(request, 'veiculos/listar_veiculo.html', {'veiculos': veiculo})

@login_required
def excluir_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    veiculo.delete()
    return redirect('listar_veiculo')

@login_required
def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('listar_veiculo')
    else:
        form = VeiculoForm(instance=veiculo)

    return render(request, 'veiculos/editar_veiculo.html', {'form': form, 'veiculo': veiculo})