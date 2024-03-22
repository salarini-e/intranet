from django.db import models

# Create your models here.
class FormIndicacaoComitePSP(models.Model):
    secretaria = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    nome = models.CharField(max_length=100, verbose_name='Nome do representante')
    matricula = models.CharField(max_length=10, verbose_name='Matrícula do representante')
    email = models.EmailField(verbose_name='Email do representante')
    telefone = models.CharField(max_length=15, verbose_name='Telefone do representante')
    observação = models.TextField('Possui alguma sugestão para pauta da comissão?')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class CadastroWebex(models.Model):
    secretaria = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    nome = models.CharField(max_length=100, verbose_name='Nome completo')    
    email = models.EmailField(verbose_name='Email')
    ramal = models.CharField(max_length=15, verbose_name='Telefone')    
    dt_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.secretaria}'