from .models import Controle
from .forms import ControleForm
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

def calcular_total_km_rodados(veiculo):
    return Controle.objects.filter(veiculo=veiculo).aggregate(Sum('km_percorrido'))['km_percorrido__sum']

def tela_controle(request):
    # consulta por período
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # consulta no intervalo
    controles = Controle.objects.all()
    if data_inicio:
        controles = controles.filter(data_saida__gte=data_inicio)
    if data_fim:
        controles = controles.filter(data_saida__lte=data_fim)

    controles = controles.order_by('-data_saida', '-hora_saida')

    return render(request, 'controle/tela_principal.html', {'controles': controles})


def visualizar_controle(request, controle_id):
    controle = get_object_or_404(Controle, pk=controle_id)

    # soma dos quilometros rodados
    total_km_rodados = Controle.objects.filter(veiculo=controle.veiculo).aggregate(Sum('km_percorrido'))['km_percorrido__sum']

    # alertar quando estiver perto da troca de óleo
    km_proxima_troca_oleo = controle.veiculo.km_troca_oleo
    percentual_aviso_troca_oleo = 80
    alerta_troca_oleo = total_km_rodados > km_proxima_troca_oleo * (percentual_aviso_troca_oleo / 100)

    return render(request, 'controle/visualizar_controle.html', {'controle': controle, 'total_km_rodados': total_km_rodados, 'alerta_troca_oleo': alerta_troca_oleo})


def editar_controle(request, controle_id):
    controle = get_object_or_404(Controle, pk=controle_id)
    total_km_rodados = calcular_total_km_rodados(controle.veiculo)
    if request.method == 'POST':
        form = ControleForm(request.POST, instance=controle)
        if form.is_valid():
            form.save()
            return redirect('tela_controle')
    else:
        form = ControleForm(instance=controle)

    return render(request, 'controle/editar_controle.html', {'form': form, 'controle': controle, 'total_km_rodados': total_km_rodados})



def excluir_controle(request, controle_id):
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.delete()
    return redirect('tela_controle')



def cadastrar_controle(request):
    if request.method == 'POST':
        form = ControleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tela_controle')
    else:
        form = ControleForm()

    return render(request, 'controle/cadastrar_controle.html', {'form': form})