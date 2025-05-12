from django import forms
from .models import Motorista

class MotoristaForm(forms.ModelForm):
    CATEGORIA_CNH_CHOICES = [
       ('', '---------'),  # Adiciona uma opção vazia
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
         # Widgets podem ser definidos aqui também, mas já estão acima.
         # Se definidos aqui, remova a definição dos campos acima.
         # widgets = {
         #     'nome': forms.TextInput(attrs={'placeholder': 'Ex: João da Silva', 'class': 'form-control'}),
         #     'telefone': forms.TextInput(attrs={'placeholder': 'Ex: (11) 91234-5678', 'class': 'form-control'}),
         #     'categoria_cnh': forms.Select(attrs={'class': 'form-control'}),  # Choices são definidos no campo acima
         #     'cpf': forms.TextInput(attrs={'placeholder': 'Ex: 12345678901', 'class': 'form-control'}),
         #     'limite_diarias': forms.NumberInput(attrs={'placeholder': 'Ex: 10', 'class': 'form-control'}),
         # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que as choices atualizadas sejam usadas
        self.fields['categoria_cnh'].choices = self.CATEGORIA_CNH_CHOICES
