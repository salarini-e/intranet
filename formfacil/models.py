from django.db import models
from .email import Email
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

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

# #############################################################################
class Opcao_Turmas(models.Model):
    dia_da_semana = models.CharField(max_length=50, verbose_name='Dia da semana')
    dia_do_mes = models.CharField(max_length=2, verbose_name='Dia do mês')
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    ativo = models.BooleanField(default=True, verbose_name='Opcao de turma ainda aberta?')

    def __str__(self):
        return f'{self.dia_da_semana}, dia {self.dia_do_mes} - das {self.hora_inicio.strftime("%H:%M")} às {self.hora_termino.strftime("%H:%M")}'

    def get_cadastros_por_turma(self):
        return Cadastro_Aulas_Processo_Digital.objects.filter(turma_escolhida=self)
    
    def get_total(self):
        return Cadastro_Aulas_Processo_Digital.objects.filter(turma_escolhida=self).count()

    def save(self, *args, **kwargs):
        hoje = datetime.now()
        dia_do_mes = int(self.dia_do_mes)
        
        # Imprime o dia atual e o dia do mês da turma no terminal
        print(f"Data atual: {hoje.strftime('%Y-%m-%d')}, Dia do mês da turma: {dia_do_mes}")
        
        # Verifica se o mês atual é maior que o mês da turma ou se é o mesmo mês mas o dia atual já passou
        if (hoje.month > hoje.month or
            (hoje.month == hoje.month and hoje.day > dia_do_mes)):
            self.ativo = False
        else:
            self.ativo = True  # Caso contrário, a turma é ativa
        
        super().save(*args, **kwargs)

class Cadastro_Aulas_Processo_Digital(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    matricula = models.CharField(max_length=6, verbose_name='Matrícula', blank=True)
    secretaria = models.CharField(max_length=250)
    setor = models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, verbose_name='Seu telefone', blank=False) 
    turma_escolhida =  models.ForeignKey(Opcao_Turmas, on_delete=models.SET_NULL, verbose_name='Selecione uma turma', null=True)
    dt_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.matricula} - {self.nome}'     
    
     
    

class Cadastro_Aulas_Treinamento_Tributario_Emissores_Taxas(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    cpf=models.CharField(max_length=14, verbose_name='CPF', unique=True, null=True)
    matricula = models.CharField(max_length=6, verbose_name='Matrícula', blank=True)
    secretaria = models.CharField(max_length=250)
    setor = models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, verbose_name='Seu telefone', blank=False) 
    dt_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.matricula} - {self.nome}'  
    
class Cadastro_Aulas_Treinamento_Tributario_Contadores(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    cpf=models.CharField(max_length=14, verbose_name='CPF', unique=True, null=True)
    matricula = models.CharField(max_length=6, verbose_name='Matrícula', blank=True)
    secretaria = models.CharField(max_length=250)
    setor = models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, verbose_name='Seu telefone', blank=False) 
    dt_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.matricula} - {self.nome}'  


