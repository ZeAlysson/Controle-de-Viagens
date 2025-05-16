from django import forms
from .models import Motorista
import re
from validate_docbr import CPF  # Importe a classe CPF

class MotoristaForm(forms.ModelForm):
    CATEGORIA_CNH_CHOICES = [
       ('', '---------'),
       ('A', 'A'),
       ('B', 'B'),
       ('C', 'C'),
       ('D', 'D'),
       ('E', 'E'),
    ]

    nome = forms.CharField(max_length=100, label="Nome", widget=forms.TextInput(attrs={'placeholder': 'Ex: João da Silva', 'class': 'form-control'}))
    telefone = forms.CharField(max_length=20, label="Telefone", widget=forms.TextInput(attrs={'placeholder': 'Ex: (11) 91234-5678', 'class': 'form-control'}))
    categoria_cnh = forms.ChoiceField(choices=CATEGORIA_CNH_CHOICES, label="Categoria CNH", widget=forms.Select(attrs={'class': 'form-control'}))
    cpf = forms.CharField(max_length=15, label="CPF", widget=forms.TextInput(attrs={'placeholder': 'Ex: 12345678901', 'class': 'form-control'}))
    limite_diarias = forms.IntegerField(label="Limite Diárias", widget=forms.NumberInput(attrs={'placeholder': 'Ex: 10', 'class': 'form-control'}))

    class Meta:
        model = Motorista
        fields = ['nome', 'telefone', 'categoria_cnh', 'cpf', 'limite_diarias']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_cnh'].choices = self.CATEGORIA_CNH_CHOICES

    def clean_cpf(self):
        cpf_valor = self.cleaned_data.get('cpf')
        cpf_validator = CPF()

        if cpf_valor:
            # Remove caracteres não numéricos para a validação e armazenamento
            cpf_numeros = re.sub(r'\D', '', cpf_valor)

            if not cpf_validator.validate(cpf_numeros):  # Usa o validador do validate_docbr
                raise forms.ValidationError("CPF inválido. Verifique os dígitos.")

            # Verifica se o CPF já existe no banco de dados,
            # excluindo a instância atual se estiver editando
            instance = getattr(self, 'instance', None)
            query_motorista = Motorista.objects.filter(cpf=cpf_numeros)
            if instance and instance.pk:
                query_motorista = query_motorista.exclude(pk=instance.pk)
            
            if query_motorista.exists():
                raise forms.ValidationError("Este CPF já está cadastrado para um motorista.")
            
            return cpf_numeros  # Retorna o CPF limpo (apenas números)
        return cpf_valor  # Retorna o valor original se estiver vazio (deixe a validação de campo obrigatório tratar)
