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
    def diarias_restantes_mes_atual(self):
        hoje = date.today()
        return self.__calcular_diarias_pelo_mes(hoje)

    def diarias_restantes_pelo_mes(self, data:date):
        return self.__calcular_diarias_pelo_mes(date)

    def __calcular_diarias_pelo_mes(self, data:date):
        viagens_do_mes = Controle.objects.filter(
            motorista=self,
            data_saida__month=data.month,
            data_saida__year=data.year
        )
        diarias = 0
        for viagem in viagens_do_mes:
            if viagem.data_saida == viagem.data_retorno:
                diarias += 0.5
                continue
            inicio_viagem = datetime.strptime(f"{viagem.data_saida}", "%Y-%m-%d")
            fim_viagem = datetime.strptime(f"{viagem.data_retorno}", "%Y-%m-%d")
            diarias += (fim_viagem.date() - inicio_viagem.date()).days + 1 

        return self.limite_diarias - diarias
        
    def __str__(self):
        return f'Motorista: {self.nome} - Tel.: {self.telefone} - CNH: {self.categoria_cnh}'