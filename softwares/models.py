from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# Create your models here.
class TipoSistema(models.Model):
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
    tipo=models.ForeignKey(TipoSistema, on_delete=models.CASCADE, verbose_name='Tipo')
    listar=models.BooleanField(default=True, verbose_name='Listar')
    # monitorar=models.BooleanField(default=True, verbose_name='Monitorar')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')    

class TipoDownload(models.Model):
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
    
    nome=models.CharField(max_length=164, verbose_name='Nome')
    descricao=models.TextField(verbose_name='Descrição')

class Downloads(models.Model):
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
    
    nome=models.CharField(max_length=164, verbose_name='Nome')
    arquivo=models.FileField(upload_to='downloads/', verbose_name='Arquivo')
    imagem=models.ImageField(upload_to='downloads/icons/', verbose_name='Imagem', null=True, blank=True)
    tamanho=models.CharField(max_length=64, verbose_name='Tamanho')
    tipo=models.ForeignKey(TipoDownload, on_delete=models.CASCADE, verbose_name='Tipo')
    descricao=models.TextField(verbose_name='Descrição')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

# Se já existe um objeto Downloads no banco de dados
@receiver(pre_save, sender=Downloads)
def update_download_file(sender, instance, **kwargs):    
    if instance.pk:
        try:            
            old_download = Downloads.objects.get(pk=instance.pk)
        except Downloads.DoesNotExist:
            return        
        if old_download.arquivo != instance.arquivo:            
            if old_download.arquivo:
                if os.path.isfile(old_download.arquivo.path):
                    os.remove(old_download.arquivo.path)

# Exclui o arquivo associado ao objeto Downloads
@receiver(pre_delete, sender=Downloads)
def delete_download_file(sender, instance, **kwargs):    
    if instance.arquivo:
        if os.path.isfile(instance.arquivo.path):            
            os.remove(instance.arquivo.path)