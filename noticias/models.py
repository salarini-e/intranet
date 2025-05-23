from django.db import models

# Create your models here.
class Carrousell(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='noticias/carrousell/')
    alt = models.CharField(max_length=100)
    link = models.CharField(max_length=200, default='#')
    data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    class meta:
        verbose_name = 'Imagem do Carrossel'
        verbose_name_plural = 'Imagens do Carrossel'

class Noticias(models.Model):

    titulo = models.CharField(max_length=150)
    imagem_capa = models.ImageField(upload_to='noticias/')
    alt_capa = models.CharField(max_length=100)
    conteudo = models.TextField()
    resumo = models.TextField(default='')
    destaque = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    class meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

class Imagens(models.Model):    
    identificacao = models.CharField(max_length=100, default='')
    imagem = models.ImageField(upload_to='noticias/imagens/')
    
    
    def __str__(self):
        return self.identificacao
    
    class meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Banco de Imagens'