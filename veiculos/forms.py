from django import forms
from veiculos.models import Veiculo  # Certifique-se de importar o modelo correspondente
import re
from brutils import is_valid_license_plate  # Importe a função de validação de placa, se necessário

class VeiculoForm(forms.ModelForm):
    #TODO ver maneira melhor
    MARCAS_CHOICES = [
        ('', '---------'), # Adiciona uma opção vazia
        ('MODELO PERSONALIZADO', 'MODELO PERSONALIZADO'),
        # Chevrolet
        ('CHEVROLET ONIX', 'CHEVROLET ONIX'),
        ('CHEVROLET PRISMA', 'CHEVROLET PRISMA'),
        ('CHEVROLET TRACKER', 'CHEVROLET TRACKER'),
        # Fiat
        ('FIAT STRADA', 'FIAT STRADA'),
        ('FIAT ARGO', 'FIAT ARGO'),
        ('FIAT MOBI', 'FIAT MOBI'),
        ('FIAT TORO', 'FIAT TORO'),
        ('FIAT PULSE', 'FIAT PULSE'),
        ('FIAT UNO', 'FIAT UNO'),
        ('FIAT CRONOS', 'FIAT CRONOS'),
        ('FIAT SIENA', 'FIAT SIENA'),
        # Volkswagen
        ('VOLKSWAGEN GOL', 'VOLKSWAGEN GOL'),
        ('VOLKSWAGEN POLO', 'VOLKSWAGEN POLO'),
        ('VOLKSWAGEN T-CROSS', 'VOLKSWAGEN T-CROSS'),
        ('VOLKSWAGEN NIVUS', 'VOLKSWAGEN NIVUS'),
        ('VOLKSWAGEN FOX', 'VOLKSWAGEN FOX'),
        ('VOLKSWAGEN VOYAGE', 'VOLKSWAGEN VOYAGE'),
        ('VOLKSWAGEN SAVEIRO', 'VOLKSWAGEN SAVEIRO'),
        # Hyundai
        ('HYUNDAI HB20', 'HYUNDAI HB20'),
        ('HYUNDAI HB20S', 'HYUNDAI HB20S'),
        ('HYUNDAI CRETA', 'HYUNDAI CRETA'),
        # Jeep
        ('JEEP RENEGADE', 'JEEP RENEGADE'),
        ('JEEP COMPASS', 'JEEP COMPASS'),
        # Toyota
        ('TOYOTA COROLLA', 'TOYOTA COROLLA'),
        ('TOYOTA ETIOS', 'TOYOTA ETIOS'),
        ('TOYOTA HILUX', 'TOYOTA HILUX'),
        # Honda
        ('HONDA FIT', 'HONDA FIT'),
        ('HONDA HR-V', 'HONDA HR-V'),
        # Renault
        ('RENAULT KWID', 'RENAULT KWID'),
        ('RENAULT SANDERO', 'RENAULT SANDERO'),
        ('RENAULT LOGAN', 'RENAULT LOGAN'),
        ]

    # Use ModelForm fields diretamente ou customize widgets se necessário
    # Os widgets definidos aqui sobrescrevem os da Meta se houver conflito
    placa = forms.CharField(max_length=7, label="Placa", widget=forms.TextInput(attrs={'placeholder': 'ABC1234', 'class': 'form-control'}))
    modelo_veiculo = forms.ChoiceField(choices=MARCAS_CHOICES, label="Marca", widget=forms.Select(attrs={'class': 'form-control'}))
    #km_troca_oleo = forms.IntegerField(label="KM Próxima Troca Óleo", widget=forms.NumberInput(attrs={'placeholder': 'Ex: 85000', 'class': 'form-control'}))
    modelo_personalizado = forms.CharField(
        required=False,
        label="Modelo Personalizado",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o modelo do veículo'})
    )


    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo_veiculo']  # Não inclua modelo_personalizado aqui

    def clean(self):
        cleaned_data = super().clean()
        modelo_veiculo = cleaned_data.get('modelo_veiculo')
        modelo_personalizado = cleaned_data.get('modelo_personalizado')

        if modelo_veiculo == 'MODELO PERSONALIZADO':
            if not modelo_personalizado:
                self.add_error('modelo_personalizado', 'Informe o modelo do veículo.')
            else:
                cleaned_data['modelo_veiculo'] = modelo_personalizado  # Salva o modelo personalizado no campo do modelo

        return cleaned_data

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