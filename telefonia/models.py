from django.db import models
from instituicoes.models import Secretaria, Setor, Servidor

class Ramal(models.Model):

    def __str__(self):
        return self.numero
    class Meta:
        verbose_name = 'Ramal'
        verbose_name_plural = 'Ramais'
    
    secretaria=models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretaria')
    setor=models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
    referencia=models.CharField(max_length=164, verbose_name='Referência')
    responsavel=models.CharField(max_length=164, verbose_name='Responsável')
    numero=models.CharField(max_length=5, verbose_name='Número')    
    
    
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')


class Telefonista(models.Model):
    
        def __str__(self):
            return self.nome
        
        class Meta:
            verbose_name = 'Telefonista'
            verbose_name_plural = 'Telefonistas'
        
        
        servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Servidor', related_name='servidor_telefonista', null=True)        
        nome=models.CharField(max_length=164, verbose_name='Nome')        
        dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
        user_inclusao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True)

        def save(self):
            if not self.nome and self.servidor:
                self.nome = self.servidor.nome 
            super(Telefonista, self).save()
