from django.db import models
from veiculos.models import Veiculo
from motoristas.models import Motorista
from servidor.models import Servidor

class Controle(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, related_name='controles')
    setor = models.CharField(max_length=50, null=True, blank=True) # Consider adding blank=True if setor can be empty
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, blank=True) # Add blank=True
    codigo_viagem = models.CharField(max_length=20, null=True, blank=True) # Add blank=True
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
        return f'Motorista: {self.motorista.nome} - Saída: {self.data_saida} {self.hora_saida} - Carro: {self.veiculo.veiculo} ({self.veiculo.marca}) - Retorno: {self.data_retorno} {self.hora_retorno}'
    
# class Estado (models.Model):
#     nome = models.CharField(max_length=50)

#     def __str__(self):
#         return f'{self.nome} - {self.sigla}'
    
# class Cidade (models.Model):
#     nome = models.CharField(max_length=50)
#     estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.nome} - {self.estado}'