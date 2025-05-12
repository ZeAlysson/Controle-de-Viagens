from django import forms
from veiculos.models import Veiculo  # Certifique-se de importar o modelo correspondente

class VeiculoForm(forms.ModelForm):
    MARCAS_CHOICES = [
        ('', '---------'), # Adiciona uma opção vazia
        ('Chevrolet', 'Chevrolet'),
        ('Fiat', 'Fiat'),
        ('Ford', 'Ford'),
        ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'),
        ('Jeep', 'Jeep'),
        ('Nissan', 'Nissan'),
        ('Peugeot', 'Peugeot'),
        ('Renault', 'Renault'),
        ('Toyota', 'Toyota'),
        ('Volkswagen', 'Volkswagen'),
        # Marcas premium/outras
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Caoa Chery', 'Caoa Chery'),
        ('Citroën', 'Citroën'),
        ('Kia', 'Kia'),
        ('Land Rover', 'Land Rover'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Mitsubishi', 'Mitsubishi'),
        ('Volvo', 'Volvo'),
        # Adicione outras marcas conforme necessário
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

