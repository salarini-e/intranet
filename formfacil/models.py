from django.db import models
from .email import Email

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
    

        
class FormSugestaoSemanaNacionalCET2024(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Seu nome completo', blank=False)
    sugestao = models.TextField(verbose_name='Deixe sua sugestão e possíveis contatos para a SNCT 2024', blank=False)
    telefone = models.CharField(max_length=15, verbose_name='Seu whatsapp', blank=False)    
    email = models.EmailField(verbose_name='Seu email')    
    dt_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.dt_inclusao}'
    
class Sistemas_EL(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
    
class CadastroEL(models.Model):
    
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    nome = models.CharField(max_length=150, verbose_name='Nome completo')
    matricula = models.CharField(max_length=10, verbose_name='Matrícula')
    telefone = models.CharField(max_length=15, verbose_name='Telefone', default='', null=True)
    email = models.EmailField(verbose_name='Email', default='', null=True)
    pdf_memorando = models.FileField(upload_to='uploads/', verbose_name='PDF do memorando')
    sistemas = models.ManyToManyField(Sistemas_EL, verbose_name='Quais sistemas você precisa de acesso?')
    observacao = models.TextField('Deseja fazer alguma observação?', blank=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

    def send_email(self):
        Email(self).cadastro_el('Novo cadastro efetuado no FormFácil - Cadastro EL', 'analise.ti.pmnf@gmail.com')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.send_email()
        except Exception as e:
            print(e)
            