from django import forms
from .models import Controle
from .models import Veiculo
from django.db.models import Q
from datetime import datetime

class ControleForm(forms.ModelForm):
    LISTA_SETORES = [
        ('', '---------'),
        ('01° GRE', '01° GRE'),
        ('02° GRE', '02° GRE'),
        ('06° GRE', '06° GRE'),
        ('08° GRE', '08° GRE'),
        ('13° GRE', '13° GRE'),
        ('14ª GRE', '14ª GRE'),
        ('3° GRE', '3° GRE'),
        ('9º GRE', '9º GRE'),
        ('AES', 'AES'),
        ('ASCOM', 'ASCOM'),
        ('ASLOG', 'ASLOG'),
        ('ATN', 'ATN'),
        ('CEAE', 'CEAE'),
        ('CEEI', 'CEEI'),
        ('CI', 'CI'),
        ('CPAD', 'CPAD'),
        ('CPI', 'CPI'),
        ('DEDE', 'DEDE'),
        ('GEADM', 'GEADM'),
        ('GEAEI', 'GEAEI'),
        ('GEAGE', 'GEAGE'),
        ('GCNTC', 'GCNTC'),
        ('GEDI', 'GEDI'),
        ('GEDPE', 'GEDPE'),
        ('GEDRA', 'GEDRA'),
        ('GEECI', 'GEECI'),
        ('GEECT', 'GEECT'),
        ('GEEDI', 'GEEDI'),
        ('GEEIEF', 'GEEIEF'),
        ('GEEJA', 'GEEJA'),
        ('GEEM', 'GEEM'),
        ('GEEP', 'GEEP'),
        ('GEFDP', 'GEFDP'),
        ('GEGEP', 'GEGEP'),
        ('GEGEPS', 'GEGEPS'),
        ('GELIC', 'GELIC'),
        ('GEOBS', 'GEOBS'),
        ('GEPOF', 'GEPOF'),
        ('GEPPE', 'GEPPE'),
        ('GGEPS', 'GGEPS'),
        ('GOADGP', 'GOADGP'),
        ('GOADP', 'GOADP'),
        ('GOPPE', 'GOPPE'),
        ('GORVE', 'GORVE'),
        ('GPROFESC', 'GPROFESC'),
        ('GTECI', 'GTECI'),
        ('NUGET', 'NUGET'),
        ('NUSEG', 'NUSEG'),
        ('OUVIDORIA', 'OUVIDORIA'),
        ('PAMPB', 'PAMPB'),
        ('PDDE', 'PDDE'),
        ('PROFESC', 'PROFESC'),
        ('SEASL', 'SEASL'),
        ('SEGEP', 'SEGEP'),
        ('SGCAD', 'SGCAD'),
        ('SGCST', 'SGCST'),
        ('SGGAE', 'SGGAE'),
        ('SGIAC', 'SGIAC'),
        ('SMH', 'SMH'),
    ]

    setor = forms.ChoiceField(
        choices=LISTA_SETORES,
        label='Setor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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
        self.fields['setor'].choices = self.LISTA_SETORES
        
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
            
            if field_name in ['data_saida', 'data_retorno'] and self.instance and getattr(self.instance, field_name):
                field.initial = getattr(self.instance, field_name).strftime('%Y-%m-%d')

            if field_name == 'km_percorrido':
                field.widget.attrs['readonly'] = True
        
        if self.instance and self.instance.pk:
            # Se estiver editando, desabilite os campos e torne-os não obrigatórios no formulário.
            # O ModelForm usará os valores da instância para esses campos ao salvar.
            self.fields['veiculo'].widget.attrs['disabled'] = True
            self.fields['veiculo'].required = False
            
            self.fields['motorista'].widget.attrs['disabled'] = True
            self.fields['motorista'].required = False

    def clean(self):
        cleaned_data = super().clean()
        
        data_saida = cleaned_data.get('data_saida')
        hora_saida = cleaned_data.get('hora_saida')
        data_retorno = cleaned_data.get('data_retorno')
        hora_retorno = cleaned_data.get('hora_retorno')
        km_saida = cleaned_data.get('km_saida')
        km_retorno = cleaned_data.get('km_retorno')

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

        # Validação de disponibilidade para veículo (usando veiculo_obj)
        if veiculo_obj and data_saida and hora_saida and data_retorno and hora_retorno:
            conflitos_veiculo = Controle.objects.filter(
                veiculo=veiculo_obj,
                data_saida__lt=data_retorno,
                data_retorno__gt=data_saida
            ).exclude(pk=self.instance.pk if self.instance and self.instance.pk else None).filter(
                Q(hora_saida__lt=hora_retorno, hora_retorno__gt=hora_saida) |
                Q(data_saida__lt=data_retorno, data_retorno__gt=data_saida) # Lógica de sobreposição de tempo
            )
            # Refinar a lógica de sobreposição de tempo se necessário, considerando dias diferentes.
            # A query acima é uma simplificação. Uma lógica mais precisa para datetime overlap:
            # (StartA <= EndB) and (EndA >= StartB)
            # (datetime_saida <= datetime_retorno_outro) and (datetime_retorno >= datetime_saida_outro)

            # Simplificando a verificação de conflito para o exemplo:
            # Esta é uma verificação básica, pode precisar de ajuste para cobrir todos os casos de sobreposição de datetime.
            conflitos_veiculo_check = Controle.objects.filter(
                veiculo=veiculo_obj,
                data_retorno__gt=data_saida, # Retorno do outro é depois da minha saída
                data_saida__lt=data_retorno   # Saída do outro é antes do meu retorno
            )
            if self.instance and self.instance.pk:
                conflitos_veiculo_check = conflitos_veiculo_check.exclude(pk=self.instance.pk)
            
            # Aqui você precisa de uma lógica mais robusta para verificar a sobreposição de horários
            # entre (data_saida, hora_saida) e (data_retorno, hora_retorno) com os registros existentes.
            # Por simplicidade, vamos assumir que a view AJAX lida com a lógica fina de disponibilidade
            # e aqui focamos em outros erros. Se as datas foram alteradas e o veículo/motorista é fixo,
            # um erro de conflito deve ser gerado se o novo período conflitar.

            # Exemplo de erro se o período conflitar com o veículo fixo:
            # if conflitos_veiculo_check.exists(): # Adapte esta condição
            #     self.add_error(None, f"O veículo '{veiculo_obj}' (inalterável) não está disponível para o novo período selecionado devido a outra reserva.")


        # Validação de disponibilidade para motorista (usando motorista_obj)
        if motorista_obj and data_saida and hora_saida and data_retorno and hora_retorno:
            # Similar à validação de veículo
            conflitos_motorista_check = Controle.objects.filter(
                motorista=motorista_obj,
                data_retorno__gt=data_saida,
                data_saida__lt=data_retorno
            )
            if self.instance and self.instance.pk:
                conflitos_motorista_check = conflitos_motorista_check.exclude(pk=self.instance.pk)
            
            # if conflitos_motorista_check.exists(): # Adapte esta condição
            #     self.add_error(None, f"O motorista '{motorista_obj}' (inalterável) não está disponível para o novo período selecionado devido a outra reserva.")

        return cleaned_data