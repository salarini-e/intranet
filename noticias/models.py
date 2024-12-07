from django.db import models

# Create your models here.
class Carrousell(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='noticias/carrousell/')
    alt = models.CharField(max_length=100)
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
    destaque = models.BooleanField(default=False)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    class meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'