from django import forms
from veiculos.models import Veiculo  # Certifique-se de importar o modelo correspondente
from brutils import is_valid_license_plate 
import re

class VeiculoForm(forms.ModelForm):
    MARCAS_CHOICES = [
        ('', '---------'), # Adiciona uma opção vazia
        # Chevrolet
        ('Chevrolet Onix', 'Chevrolet Onix'),
        # Fiat
        ('Fiat Strada', 'Fiat Strada'),
        ('Fiat Argo', 'Fiat Argo'),
        ('Fiat Mobi', 'Fiat Mobi'),
        ('Fiat Toro', 'Fiat Toro'),
        ('Fiat Pulse', 'Fiat Pulse'),
        # Volkswagen
        ('Volkswagen Gol', 'Volkswagen Gol'), # Embora descontinuado, ainda popular
        ('Volkswagen Polo', 'Volkswagen Polo'),
        ('Volkswagen T-Cross', 'Volkswagen T-Cross'),
        ('Volkswagen Nivus', 'Volkswagen Nivus'),
        # Hyundai
        ('Hyundai HB20', 'Hyundai HB20'),
        ('Hyundai HB20S', 'Hyundai HB20S'),
        # Jeep
        ('Jeep Renegade', 'Jeep Renegade'),
    ]

    # Use ModelForm fields diretamente ou customize widgets se necessário
    # Os widgets definidos aqui sobrescrevem os da Meta se houver conflito
    placa = forms.CharField(max_length=7, label="Placa", widget=forms.TextInput(attrs={'placeholder': 'ABC1234', 'class': 'form-control'}))
    modelo_veiculo = forms.ChoiceField(choices=MARCAS_CHOICES, label="Marca", widget=forms.Select(attrs={'class': 'form-control'}))
    #km_troca_oleo = forms.IntegerField(label="KM Próxima Troca Óleo", widget=forms.NumberInput(attrs={'placeholder': 'Ex: 85000', 'class': 'form-control'}))

    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo_veiculo']
        # Widgets podem ser definidos aqui também, mas já estão acima.
        # Se definidos aqui, remova a definição dos campos acima.
        # widgets = {
        #     'placa': forms.TextInput(attrs={'placeholder': 'ABC1234', 'class': 'form-control'}),
        #     'marca': forms.Select(attrs={'class': 'form-control'}), # Choices são definidos no campo acima
        #     'veiculo': forms.TextInput(attrs={'placeholder': 'Ex: Onix, Corolla, Renegade', 'class': 'form-control'}),
        #     'km_troca_oleo': forms.NumberInput(attrs={'placeholder': 'Ex: 85000', 'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que as choices atualizadas sejam usadas
        self.fields['modelo_veiculo'].choices = self.MARCAS_CHOICES

    def clean_placa(self):
        placa_valor = self.cleaned_data.get('placa')

        if placa_valor:
            # Remove caracteres não alfanuméricos e converte para maiúsculas.
            # A brutils.placa.is_valid também faz limpeza, mas é bom padronizar aqui.
            placa_limpa = re.sub(r'[^A-Z0-9]', '', str(placa_valor).upper())

            # A função is_valid da brutils já verifica o comprimento e o formato.
            if not is_valid_license_plate(placa_limpa):
                raise forms.ValidationError(
                    "Formato de placa inválido. Use AAA1234 ou AAA1A23 (Mercosul) e verifique os caracteres."
                )

            # Verifica se a placa já existe no banco de dados,
            # excluindo a instância atual se estiver editando
            instance = getattr(self, 'instance', None)
            query = Veiculo.objects.filter(placa=placa_limpa) # Use a placa_limpa para a consulta
            if instance and instance.pk:
                query = query.exclude(pk=instance.pk)

            if query.exists():
                raise forms.ValidationError("Esta placa já está cadastrada.")

            return placa_limpa # Retorna a placa limpa e padronizada

        # Se o campo puder ser opcional e vazio for válido, retorne placa_valor.
        return placa_valor