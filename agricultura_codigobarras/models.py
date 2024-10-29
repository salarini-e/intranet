from django.db import models
from instituicoes.models import Servidor
from django.utils.crypto import get_random_string

class User_Agricultura(models.Model):
    servidor = models.OneToOneField(Servidor, on_delete=models.CASCADE)
    autoriazado = models.BooleanField(default=True)
    def __str__(self):
       
        return f"Servidor - {self.servidor}"
class Equipamento(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição do Equipamento")
    numero_convenio = models.CharField(max_length=50, unique=True, verbose_name="Número do Convênio")
    codigo_barra = models.CharField(max_length=22, unique=True, editable=False)

    def save(self, *args, **kwargs):
               # Primeiro salvamento para gerar o ID
        if not self.codigo_barra:
            super().save(*args, **kwargs)
            # Gera o código de barras usando o ID
            hash_numerico = get_random_string(length=22, allowed_chars='0123456789')
            self.codigo_barra = f"{hash_numerico}"
        
        # Segundo salvamento com o código de barras
        super().save(*args, **kwargs)
        
    def get_codigo(self):
        return str(self.id).zfill(6)

    def __str__(self):
        codigo = self.get_codigo() if self.id else "ID ainda não gerado"
        return f"{self.descricao} - Convênio: {self.numero_convenio} - Código de Barras: {self.codigo_barra} - id: {codigo}"
    
