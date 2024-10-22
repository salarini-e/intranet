from django.db import models
from autenticacao.models import User
import os 

# Create your models here.
class Topico(models.Model):
    nome = models.CharField(max_length=164, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    dt_inclusao = models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Usuário de inclusão')
    palavras_chave = models.CharField(max_length=164, verbose_name='Palavras chaves')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
    
    def get_codigo(self):
        return str(self.id).zfill(6)



class Subtopico(models.Model):
    TIPO_CHOICES = (
        ('ytb','youtube'),
        ('pdf', 'pdf'),
        ('txt', 'texto'),
    )
    topico = models.ForeignKey(Topico, on_delete=models.DO_NOTHING, verbose_name='Tópico associado')
    tema = models.CharField(max_length=164, verbose_name='Tema')
    tipo = models.CharField(max_length=3, verbose_name='Tipo', choices=TIPO_CHOICES)
    dt_inclusao= models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Usuário de inclusão')
    
    def __str__(self):
        return self.tema   
    
    

    def get_codigo(self):
        return str(self.id).zfill(6)


class Arquivo_GoogleDrive(models.Model):
    subtopico = models.ForeignKey(Subtopico, on_delete=models.DO_NOTHING, verbose_name='Subtópico Associado')
    iframe = models.TextField(verbose_name='HTML do iframe')

class Arquivo_Texto(models.Model):
    subtopico = models.ForeignKey(Subtopico, on_delete=models.DO_NOTHING, verbose_name='Subtópico Associado')
    texto = models.TextField(verbose_name='Texto')

    def __str__(self):
        return self.texto  


class Arquivo_PDF(models.Model):
    subtopico = models.ForeignKey(Subtopico, on_delete=models.DO_NOTHING, verbose_name='Subtópico Associado')
    texto = models.TextField(verbose_name='Título')
    arquivo_pdf = models.FileField(upload_to='pdfs/', verbose_name='Arquivo PDF')

    def save_file(file):
        safe_name = os.path.basename(file.name).encode('utf-8').decode('utf-8')
        return super()._save(safe_name, file)
    def __str__(self):
        return self.texto