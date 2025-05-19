from django import forms
from .models import Controle
from .models import Veiculo
from django.db.models import Q
from datetime import datetime

class ControleForm(forms.ModelForm):
    class Meta:
        model = Controle
        widgets = {
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
            'data_retorno': forms.DateInput(attrs={'type': 'date'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
            'hora_retorno': forms.TimeInput(attrs={'type': 'time'}),
        }
        fields = [
            'veiculo',
            'motorista',
            'setor',
            'servidor',
            'codigo_viagem',
            'data_saida',
            'hora_saida',
            'km_saida',
            'destino',
            'data_retorno',
            'hora_retorno',
            'km_retorno',
            'km_percorrido'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        
        veiculo = cleaned_data.get('veiculo')
        motorista = cleaned_data.get('motorista')
        data_saida = cleaned_data.get('data_saida')
        hora_saida = cleaned_data.get('hora_saida')
        data_retorno = cleaned_data.get('data_retorno')
        hora_retorno = cleaned_data.get('hora_retorno')

        # Se campos essenciais para esta validação estiverem faltando, retorne (erros anteriores serão tratados)
        if not all([veiculo, motorista, data_saida, hora_saida, data_retorno, hora_retorno]):
            return cleaned_data

        # Combina data e hora para a nova/editada entrada
        try:
            new_start_dt = datetime.combine(data_saida, hora_saida)
            new_end_dt = datetime.combine(data_retorno, hora_retorno)
        except TypeError:
            # Isso não deve acontecer se os campos forem DateField e TimeField e forem obrigatórios
            raise forms.ValidationError("Data ou hora fornecida está em formato inválido.")

        if new_start_dt >= new_end_dt:
            self.add_error('data_retorno', "A data/hora de retorno deve ser posterior à data/hora de saída.")
            self.add_error('hora_retorno', "A data/hora de retorno deve ser posterior à data/hora de saída.")
            return cleaned_data # Retorna para exibir este e outros erros potenciais

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
        
        print("ESTOU SAINDO DO CLEAN")
        return cleaned_data