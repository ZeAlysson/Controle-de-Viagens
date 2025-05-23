from datetime import date
from django.db import models
from veiculos.models import Veiculo

class Setor(models.Model):
    setor = models.CharField(max_length=100, null=False, blank=False)
    sigla = models.CharField(max_length=20, null=False, blank=False)
    cidade = models.CharField(max_length=30, null= False, blank=False)

    def __str__(self):
        return f'{self.sigla} - {self.cidade}'

class Controle(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey("motoristas.Motorista", on_delete=models.SET_NULL, null=True, related_name='controles')
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True)
    servidor = models.CharField(max_length=100)
    codigo_viagem = models.CharField(max_length=20, null=True, blank=True) # Add blank=True
    data_saida = models.DateField()
    hora_saida = models.TimeField()
    km_saida = models.IntegerField(null=True, blank=True) # Add blank=True
    destino = models.CharField(max_length=100)
    data_retorno = models.DateField()
    hora_retorno = models.TimeField()
    km_retorno = models.IntegerField(null=True, blank=True) # Add blank=True
    km_percorrido = models.IntegerField(null=True, blank=True) # Add blank=True


    @property
    def quantidade_diarias(self) -> float:
        return self.calcular_diarias_entre_datas(self.data_saida, self.data_retorno)

    @staticmethod
    def calcular_diarias_entre_datas(data_saida:date, data_retorno:date) -> float:
        if data_saida == data_retorno:
            return 0.5
        else:
            return (data_retorno - data_saida).days + 1

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