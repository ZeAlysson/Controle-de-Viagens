from django.db import models



class Motorista(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    categoria_cnh = models.CharField(max_length=20)
    cpf = models.CharField(primary_key=True, max_length=11, unique=True, null=False)
    limite_diarias = models.IntegerField(default=0)

    def __str__(self):
        return f'Motorista: {self.nome} - Tel.: {self.telefone} - CNH: {self.cnh}'