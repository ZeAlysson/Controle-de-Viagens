from django import forms

class VeiculoForm(forms.Form):
    MARCAS_CHOICES = [
        ('ford', 'Ford'),
        ('chevrolet', 'Chevrolet'),
        ('toyota', 'Toyota'),
        ('honda', 'Honda'),
        ('volkswagen', 'Volkswagen'),
    ]
    
    # Campos do formulário
    placa = forms.CharField(max_length=7, label="Placa", widget=forms.TextInput(attrs={'placeholder': 'ABC1234'}))
    marca = forms.ChoiceField(choices=MARCAS_CHOICES, label="Marca")
    veiculo = forms.CharField(max_length=50, label="Veículo", widget=forms.TextInput(attrs={'placeholder': 'Ex: Civic'}))
    km_troca_oleo = forms.IntegerField(label="KM troca óleo", widget=forms.NumberInput(attrs={'placeholder': 'Ex: 10000'}))