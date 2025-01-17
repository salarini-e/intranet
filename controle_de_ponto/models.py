from django.db import models
from django.contrib.auth.models import User
from instituicoes.models import Secretaria, Setor, Servidor

# class Responsavel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
from datetime import datetime, timedelta

class Registro(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    matricula = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, null=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, null=True, blank=True)
    entrada1 = models.TimeField()
    saida1 = models.TimeField(null=True, blank=True)
    entrada2 = models.TimeField(null=True, blank=True)
    saida2 = models.TimeField(null=True, blank=True)
    data_registro = models.DateField()

    def __str__(self):
        return f"Registro de {self.nome} em {self.data_registro}"

    def servidor(self):
        return Servidor.objects.filter(user=self.user).first()
    
    def servidor_nome(self):
        return self.servidor().nome
    
    def save(self, *args, **kwargs):
        self.matricula = self.servidor().matricula
        self.nome = self.servidor_nome()
        super().save(*args, **kwargs)

    def total_horas(self):
        total = timedelta()

        # Converter os horários em objetos datetime para fazer o cálculo
        if self.entrada1 and self.saida1:
            entrada1_dt = datetime.combine(self.data_registro, self.entrada1)
            saida1_dt = datetime.combine(self.data_registro, self.saida1)
            total += saida1_dt - entrada1_dt

        if self.entrada2 and self.saida2:
            entrada2_dt = datetime.combine(self.data_registro, self.entrada2)
            saida2_dt = datetime.combine(self.data_registro, self.saida2)
            total += saida2_dt - entrada2_dt

        # Retornar o total de horas como string formatada (hh:mm)
        horas, segundos = divmod(total.total_seconds(), 3600)
        minutos = segundos // 60
        result = f"{int(horas)}h {int(minutos)}m"
        # print(result)
        return result