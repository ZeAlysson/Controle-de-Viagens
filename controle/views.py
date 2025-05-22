from calendar import monthrange
from motoristas.models import Motorista
from veiculos.models import Veiculo
from .models import Controle
from .forms import ControleForm
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from datetime import datetime, date

def calcular_total_km_rodados(veiculo):
    return Controle.objects.filter(veiculo=veiculo).aggregate(Sum('km_percorrido'))['km_percorrido__sum']

@login_required
@user_passes_test(lambda u: u.is_superuser)
def tela_controle(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    controles = Controle.objects.all()
    if data_inicio:
        controles = controles.filter(data_saida=data_inicio)
    if data_fim:
        controles = controles.filter(data_saida__lte=data_fim)

    controles = controles.order_by('-data_saida', '-hora_saida')

    return render(
        request,
        'controle/tela_principal.html',
        {
            'controles': controles,
            'today': date.today().isoformat(),
        }
    )

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
            print(form.errors)
    else:
        form = ControleForm()

    return render(request, 'controle/cadastrar_controle.html', {'form': form})

@require_GET
@user_passes_test(lambda u: u.is_superuser)
def verificar_disponibilidade(request):
    
    data_saida = request.GET.get('data_saida')
    data_retorno = request.GET.get('data_retorno')
    id_controle = request.GET.get('id_controle')

    if not all([data_saida, data_retorno]):
        return JsonResponse({'error': 'Dados incompletos.'}, status=400)

    try:
        data_saida = datetime.strptime(f"{data_saida}", "%Y-%m-%d")
        data_retorno = datetime.strptime(f"{data_retorno}", "%Y-%m-%d")                                                                                               
    except ValueError:
        return JsonResponse({'error': 'Formato de data ou hora inválido.'}, status=400)

    if data_saida > data_retorno:
        return JsonResponse({'error': 'Data de saída deve ser antes da de retorno.'}, status=400)
    
    quantidade_diaria_nova_viagem = Controle.calcular_diarias_entre_datas(data_saida, data_retorno)

    controles_conflitantes = filtrar_controles_conflitantes(data_saida, data_retorno)

    veiculos_ocupados = controles_conflitantes.values_list('veiculo_id', flat=True)
    motoristas_ocupados = controles_conflitantes.values_list('motorista_id', flat=True)

    veiculos_disponiveis = Veiculo.objects.exclude(id__in=veiculos_ocupados).order_by("modelo_veiculo")
    motoristas_sem_conflitos_datas = Motorista.objects.exclude(id__in=motoristas_ocupados).order_by("nome")

    motoristas_disponiveis = None
    if(id_controle is None):
        motoristas_disponiveis = filtrar_motoristas_com_diarias_disponiveis(motoristas_sem_conflitos_datas, quantidade_diaria_nova_viagem)
    else:
        controle = Controle.objects.get(id=id_controle)
        motoristas_disponiveis = filtrar_motoristas_com_diarias_disponiveis(motoristas_sem_conflitos_datas, quantidade_diaria_nova_viagem, data_saida , controle)

    return JsonResponse({
    'veiculos': [{'id': v.id, 'nome': str(v)} for v in veiculos_disponiveis],
    'motoristas': [{'id': m.id, 'nome': str(m)} for m in motoristas_disponiveis],
    })

def filtrar_controles_conflitantes(data_saida, data_retorno):
    conflito = (
        Q(data_retorno__gt=data_saida.date()) |
        Q(data_retorno=data_saida.date())
    ) & (
        Q(data_saida__lt=data_retorno.date()) |
        (Q(data_saida=data_retorno.date()))
    )
    return Controle.objects.filter(conflito)

def filtrar_motoristas_com_diarias_disponiveis(motoristas, quantidade_diaria_nova_viagem, data_nova_viagem:date, controle:Controle=None):
    motoristas_disponiveis = []
    if controle != None:
        motorista_da_viagem = controle.motorista
        diferença_entre_diarias = quantidade_diaria_nova_viagem - controle.quantidade_diarias
        if diferença_entre_diarias > 0:
            if diferença_entre_diarias <= motorista_da_viagem.diarias_restantes_pelo_mes(data_nova_viagem):
                motoristas_disponiveis.append(motorista_da_viagem)
        else:
            motoristas_disponiveis.append(motorista_da_viagem)
            
        if (controle.quantidade_diarias - quantidade_diaria_nova_viagem) < motorista_da_viagem.diarias_restantes_pelo_mes(controle.data_saida):
            motoristas_disponiveis.append(motorista_da_viagem)
    for motorista in motoristas:
        if motorista.diarias_restantes_mes_atual >= quantidade_diaria_nova_viagem:
            motoristas_disponiveis.append(motorista)
    return motoristas_disponiveis
