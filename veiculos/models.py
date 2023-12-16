from django.db import models



class Veiculo(models.Model):
    placa = models.CharField(max_length=20)
    marca = models.CharField(max_length=50)
    veiculo = models.CharField(max_length=50)
    km_troca_oleo = models.IntegerField()

    def __str__(self):
            return f'{self.veiculo} - Placa: {self.placa} - Troca oleo: {self.km_troca_oleo} Km'