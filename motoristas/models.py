from django.db import models



class Motorista(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    cnh = models.CharField(max_length=20)

    def __str__(self):
        return f'Motorista: {self.nome} - Tell: {self.telefone} - CNH: {self.cnh}'