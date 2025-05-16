from datetime import date
from django.db import models
from datetime import datetime, timedelta, date, datetime as dt
from controle.models import Controle


class Motorista(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    categoria_cnh = models.CharField(max_length=20)
    cpf = models.CharField(max_length=15, unique=True, null=False)
    limite_diarias = models.IntegerField(default=0)

    @property
    def diarias_restantes(self):
        hoje = date.today()
        viagens_do_mes = Controle.objects.filter(
            motorista=self,
            data_saida__month=hoje.month,
            data_saida__year=hoje.year
        )

        diarias = 0
        for viagem in viagens_do_mes:
            if viagem.data_saida == viagem.data_retorno:
                diarias += 0.5
                continue
            diarias += 1

        return self.limite_diarias - diarias

    def __str__(self):
        return f'Motorista: {self.nome} - Tel.: {self.telefone} - CNH: {self.categoria_cnh}'