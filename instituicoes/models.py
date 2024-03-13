from django.db import models

class Secretaria(models.Model):
   
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Secretaria'
        verbose_name_plural = 'Secretarias'
    
    nome=models.CharField(max_length=64, verbose_name='Nome')
    sigla=models.CharField(max_length=8, verbose_name='Sigla')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

class Setor(models.Model):
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
    
    nome=models.CharField(max_length=64, verbose_name='Nome')
    sigla=models.CharField(max_length=8, verbose_name='Sigla')
    secretaria=models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretaria')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
