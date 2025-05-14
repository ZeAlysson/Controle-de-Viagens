from django.shortcuts import get_object_or_404, redirect, render
from controle.models import Controle
from servidor.forms import ServidorForm
from servidor.models import Servidor
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def cadastrar_servidor(request):
    if request.method == 'POST':
        form = ServidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servidores')
    else:
        form = ServidorForm()

    return render(request, 'servidor/cadastrar_servidor.html', {'form': form})

@login_required
def listar_servidores(request):
    servidores = Servidor.objects.all()
    return render(request, 'servidor/listar_servidores.html', {'servidores': servidores})

@login_required
def excluir_servidor(request, servidor_cpf):
    servidor = get_object_or_404(Servidor, pk=servidor_cpf)
    servidor.delete()
    return redirect('listar_servidores')

@login_required
def editar_servidor(request, servidor_cpf):
    servidor = get_object_or_404(Servidor, pk=servidor_cpf)

    if request.method == 'POST':
        form = ServidorForm(request.POST, instance=servidor)
        if form.is_valid():
            form.save()
            return redirect('listar_servidores')
    else:
        form = ServidorForm(instance=servidor)
    return render(request, 'servidor/editar_servidor.html', {'form': form, 'servidor': servidor})