from django.db import models
from veiculos.models import Veiculo
from motoristas.models import Motorista

class Controle(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True)
    data_saida = models.DateField()
    hora_saida = models.TimeField()
    km_saida = models.IntegerField()
    destino = models.CharField(max_length=100)
    data_retorno = models.DateField()
    hora_retorno = models.TimeField()
    km_retorno = models.IntegerField()
    km_percorrido = models.IntegerField()

    def formato_data_saida(self):
        return self.data_saida.strftime("%Y-%m-%d")

    def formato_data_retorno(self):
        return self.data_retorno.strftime("%Y-%m-%d")

    def __str__(self):
        return f'Motorista: {self.motorista.nome} - Saida: {self.data_saida} {self.hora_saida} - Carro: {self.veiculo.veiculo} ({self.veiculo.marca}) - Retorno: {self.data_retorno} {self.hora_retorno}'