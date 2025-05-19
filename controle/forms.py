from django import forms
from .models import Controle
from .models import Veiculo
from django.db.models import Q
from datetime import datetime

class ControleForm(forms.ModelForm):
    class Meta:
        model = Controle
        widgets = {
            'data_saida': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_retorno': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
            'hora_retorno': forms.TimeInput(attrs={'type': 'time'}),
        }
        fields = [
            'veiculo', 'motorista', 'setor', 'servidor', 'codigo_viagem',
            'data_saida', 'hora_saida', 'km_saida', 'destino',
            'data_retorno', 'hora_retorno', 'km_retorno', 'km_percorrido'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
               

    def clean(self):
        cleaned_data = super().clean()
        
        data_saida = cleaned_data.get('data_saida')
        hora_saida = cleaned_data.get('hora_saida')
        data_retorno = cleaned_data.get('data_retorno')
        hora_retorno = cleaned_data.get('hora_retorno')
        km_saida = cleaned_data.get('km_saida')
        km_retorno = cleaned_data.get('km_retorno')
        veiculo = cleaned_data.get('veiculo')
        motorista = cleaned_data.get('motorista')

        # Obter veículo e motorista corretamente para validação
        # Se estiver editando, os campos foram marcados como required=False,
        # então cleaned_data.get() pode retornar None. Usar os da instância.
        veiculo_obj = cleaned_data.get('veiculo')
        if self.instance and self.instance.pk and not veiculo_obj:
            veiculo_obj = self.instance.veiculo
            # Opcional: adicionar de volta ao cleaned_data se outras partes do clean dependerem disso
            # cleaned_data['veiculo'] = veiculo_obj 

        motorista_obj = cleaned_data.get('motorista')
        if self.instance and self.instance.pk and not motorista_obj:
            motorista_obj = self.instance.motorista
            # cleaned_data['motorista'] = motorista_obj

        # Validação de Data/Hora
        if data_saida and hora_saida and data_retorno and hora_retorno:
            datetime_saida = datetime.combine(data_saida, hora_saida)
            datetime_retorno = datetime.combine(data_retorno, hora_retorno)
            if datetime_retorno <= datetime_saida:
                self.add_error('data_retorno', "A data/hora de retorno deve ser posterior à data/hora de saída.")
                self.add_error('hora_retorno', " ") # Adiciona erro ao campo para destaque

        # Validação de KM
        if km_saida is not None and km_retorno is not None and km_retorno <= km_saida:
            self.add_error('km_retorno', "Km de retorno deve ser maior que Km de saída.")

       # Consulta base para controles existentes
        base_query = Controle.objects.all()
        # Se estiver editando uma instância existente, exclua-a da verificação de conflito
        if self.instance and self.instance.pk:
            base_query = base_query.exclude(pk=self.instance.pk)

        # Condição de sobreposição: (FimExistente > NovoInício) E (InícioExistente < NovoFim)
        # FimExistente > NovoInício
        q_existing_end_gt_new_start = (
            Q(data_retorno__gt=data_saida) |
            (Q(data_retorno=data_saida) & Q(hora_retorno__gt=hora_saida))
        )
        # InícioExistente < NovoFim
        q_existing_start_lt_new_end = (
            Q(data_saida__lt=data_retorno) |
            (Q(data_saida=data_retorno) & Q(hora_saida__lt=hora_retorno))
        )
        
        overlap_condition = q_existing_end_gt_new_start & q_existing_start_lt_new_end

        # Verifica sobreposição de veículo
        conflicting_veiculo_qs = base_query.filter(veiculo=veiculo).filter(overlap_condition)
        if conflicting_veiculo_qs.exists():
            conflict = conflicting_veiculo_qs.first()
            error_msg = (
                f"Veículo '{veiculo}' já está agendado em um período conflitante: "
                f"de {conflict.data_saida.strftime('%d/%m/%Y')} {conflict.hora_saida.strftime('%H:%M')} "
                f"até {conflict.data_retorno.strftime('%d/%m/%Y')} {conflict.hora_retorno.strftime('%H:%M')}."
            )
            self.add_error('veiculo', error_msg)

        # Verifica sobreposição de motorista
        conflicting_motorista_qs = base_query.filter(motorista=motorista).filter(overlap_condition)
        if conflicting_motorista_qs.exists():
            conflict = conflicting_motorista_qs.first()
            error_msg = (
                f"'{motorista}' já está agendado em um período conflitante: "
                f"de {conflict.data_saida.strftime('%d/%m/%Y')} {conflict.hora_saida.strftime('%H:%M')} "
                f"até {conflict.data_retorno.strftime('%d/%m/%Y')} {conflict.hora_retorno.strftime('%H:%M')}."
            )
            self.add_error('motorista', error_msg)

        return cleaned_data