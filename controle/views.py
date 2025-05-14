from motoristas.models import Motorista
from veiculos.models import Veiculo
from .models import Controle
from .forms import ControleForm
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from datetime import datetime

def calcular_total_km_rodados(veiculo):
    return Controle.objects.filter(veiculo=veiculo).aggregate(Sum('km_percorrido'))['km_percorrido__sum']

@login_required
@user_passes_test(lambda u: u.is_superuser)
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def visualizar_controle(request, controle_id):
    controle = get_object_or_404(Controle, pk=controle_id)

    # soma dos quilometros rodados
    total_km_rodados = Controle.objects.filter(veiculo=controle.veiculo).aggregate(Sum('km_percorrido'))['km_percorrido__sum']

    # alertar quando estiver perto da troca de óleo
    km_proxima_troca_oleo = controle.veiculo.km_troca_oleo
    percentual_aviso_troca_oleo = 80
    alerta_troca_oleo = total_km_rodados > km_proxima_troca_oleo * (percentual_aviso_troca_oleo / 100)

    return render(request, 'controle/visualizar_controle.html', {'controle': controle, 'total_km_rodados': total_km_rodados, 'alerta_troca_oleo': alerta_troca_oleo})

@login_required
@user_passes_test(lambda u: u.is_superuser)
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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def excluir_controle(request, controle_id):
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.delete()
    return redirect('tela_controle')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastrar_controle(request):
    if request.method == 'POST':
        form = ControleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tela_controle')
    else:
        form = ControleForm()

    return render(request, 'controle/cadastrar_controle.html', {'form': form})

@require_GET
def verificar_disponibilidade(request):
    data_saida = request.GET.get('data_saida')
    hora_saida = request.GET.get('hora_saida')
    data_retorno = request.GET.get('data_retorno')
    hora_retorno = request.GET.get('hora_retorno')

    if not all([data_saida, hora_saida, data_retorno, hora_retorno]):
        return JsonResponse({'error': 'Dados incompletos.'}, status=400)

    try:
        inicio = datetime.strptime(f"{data_saida} {hora_saida}", "%Y-%m-%d %H:%M")
        fim = datetime.strptime(f"{data_retorno} {hora_retorno}", "%Y-%m-%d %H:%M")
    except ValueError:
        return JsonResponse({'error': 'Formato de data ou hora inválido.'}, status=400)

    if inicio >= fim:
        return JsonResponse({'error': 'Data de saída deve ser antes da de retorno.'}, status=400)

    # Filtra controles que conflitam com o novo período
    conflito = (
        Q(data_retorno__gt=inicio.date()) |
        (Q(data_retorno=inicio.date()) & Q(hora_retorno__gt=inicio.time()))
    ) & (
        Q(data_saida__lt=fim.date()) |
        (Q(data_saida=fim.date()) & Q(hora_saida__lt=fim.time()))
    )

    controles_conflitantes = Controle.objects.filter(conflito)

    veiculos_ocupados = controles_conflitantes.values_list('veiculo_id', flat=True)
    motoristas_ocupados = controles_conflitantes.values_list('motorista_id', flat=True)

    veiculos_disponiveis = Veiculo.objects.exclude(id__in=veiculos_ocupados)
    motoristas_disponiveis = Motorista.objects.exclude(id__in=motoristas_ocupados)

    return JsonResponse({
    'veiculos': [{'id': v.id, 'nome': str(v)} for v in veiculos_disponiveis],
    'motoristas': [{'id': m.id, 'nome': str(m)} for m in motoristas_disponiveis],
})