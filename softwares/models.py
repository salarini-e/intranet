from django.db import models

# Create your models here.
class Tipo(models.Model):
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
    
    nome=models.CharField(max_length=164, verbose_name='Nome')
    descricao=models.TextField(verbose_name='Descrição')

class Sistemas(models.Model):
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Sistema'
        verbose_name_plural = 'Sistemas'
    
    nome=models.CharField(max_length=164, verbose_name='Nome')
    url=models.URLField(max_length=200, verbose_name='URL')
    descricao=models.TextField(verbose_name='Descrição')
    tipo=models.ForeignKey(Tipo, on_delete=models.CASCADE, verbose_name='Tipo')
    listar=models.BooleanField(default=True, verbose_name='Listar')
    # monitorar=models.BooleanField(default=True, verbose_name='Monitorar')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')    
        
