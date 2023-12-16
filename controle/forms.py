from django import forms
from .models import Controle


class ControleForm(forms.ModelForm):
    class Meta:
        model = Controle
        widgets = {
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
            'data_retorno': forms.DateInput(attrs={'type': 'date'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
            'hora_retorno': forms.TimeInput(attrs={'type': 'time'}),
        }
        fields = '__all__'


    