from django.db import models

class Servidor(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11, unique=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    

    def __str__(self):
        return f'Servidor: {self.nome} - Tel.: {self.telefone} - CPF: {self.cpf}'
