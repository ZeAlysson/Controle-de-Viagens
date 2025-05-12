from django import forms
from .models import Controle


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
        self.fields['setor'].choices = self.LISTA_SETORES
        # Adiciona a classe form-control para outros campos que não são widgets diretos, se necessário
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

    