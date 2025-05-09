from django.db import models

class Veiculo(models.Model):
    placa = models.CharField(max_length=7)
    modelo_veiculo = models.CharField(max_length=50)


    def __str__(self):
            return f'{self.modelo_veiculo} - Placa: {self.placa}'