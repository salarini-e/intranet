from django.db import models
from instituicoes.models import Secretaria, Setor

# Create your models here.
class Ramal(models.Model):

    def __str__(self):
        return self.numero
    class Meta:
        verbose_name = 'Ramal'
        verbose_name_plural = 'Ramais'
    
    secretaria=models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretaria')
    setor=models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
    referencia=models.CharField(max_length=64, verbose_name='Referência')
    numero=models.CharField(max_length=4, verbose_name='Número')
    webex=models.CharField(max_length=64, verbose_name='Webex', blank=True, null=True)
    
    
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')