from django.db import models
from .email import Email
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.core.exceptions import ValidationError

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
        if (hoje.month > hoje.month or
            (hoje.month == hoje.month and hoje.day > dia_do_mes)):
            self.ativo = False
        else:
            self.ativo = True 
        
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

class Inscricao_Decretos_Portaria_E_Atos_Do_Prefeito(models.Model):
    HORARIOS_CHOICES = (        
        ('14:00', '14:00'),
        ('16:00', '16:00'),        
    )
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    cpf=models.CharField(max_length=14, verbose_name='CPF', unique=True, null=True)
    matricula = models.CharField(max_length=6, verbose_name='Matrícula', blank=True)
    secretaria = models.CharField(max_length=250)
    setor = models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, verbose_name='Seu telefone', blank=False) 
    horarios = models.CharField(max_length=5, choices=HORARIOS_CHOICES, verbose_name='Horários disponíveis')    
    dt_registro = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.matricula} - {self.nome}'  

    @classmethod
    def get_qnt_inscritos(cls):
        qnt = {}
        for horario, _ in cls.HORARIOS_CHOICES:
            count = cls.objects.filter(horarios=horario).count()
            qnt[horario] = count < 7  # True se ainda há vagas, False caso contrário
        return qnt
    
    def filtrar_por_horario(self, horario):
        return self.objects.filter(horarios=horario)
    
    def get_total(self):
        return self.objects.all().count()

#Cadastro de Almoxarifado
class Cadastro_de_Almoxarifado(models.Model):
    nome_requisitante = models.CharField(max_length=150, verbose_name='Nome de quem pode requisitar')
    matricula = models.CharField(max_length=10, verbose_name='Matrícula')
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    secretaria = models.CharField(max_length=250, verbose_name='Secretaria')
    autorizador = models.CharField(max_length=150, verbose_name='Quem autoriza a solicitação')
    responsavel_material = models.CharField(max_length=150, verbose_name='Quem pega os materiais')
    dt_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome_requisitante} - {self.secretaria}'

class AvaliacaoSistemaEL(models.Model):
    sistema = models.CharField(max_length=100, verbose_name='Sistema Avaliado')  # Removed choices
    usuario_nome = models.CharField(max_length=150, verbose_name='Nome do Usuário')
    usuario_matricula = models.CharField(max_length=10, verbose_name='Matrícula do Usuário')    
    satisfacao = models.IntegerField(verbose_name='Nível de Satisfação (1 a 5)', null=True, blank=True)
    houve_lentidao = models.IntegerField(verbose_name='Avaliação o tempo de resposta do sistema ', null=True, blank=True)    
    sugestao = models.TextField(verbose_name='Sugestão', blank=True, null=True)

    data_avaliacao = models.DateTimeField(auto_now_add=True)
    usuario_inclusao = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Usuário que incluiu', null=True, blank=True) 

    def __str__(self):
        return f'{self.sistema} - {self.usuario_nome}'


class SolicitacaoEmailInstitucional(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome completo')
    matricula = models.CharField(max_length=10, verbose_name='Matrícula')
    cpf = models.CharField(max_length=14, verbose_name='CPF')    
    telefone = models.CharField(max_length=15, verbose_name='Telefone', null=True)
    secretaria = models.CharField(max_length=250, verbose_name='Secretaria')
    email_institucional = models.EmailField(verbose_name='E-mail institucional sugerido. Sugestão no formato: nome.sobrenome@prefeituradenovafriburgo.rj.gov.br')
    dt_registro = models.DateTimeField(auto_now_add=True)

class ProcessoDigitalInscricao(models.Model):
    TURMAS = (
        ("turma1", "Turma 1 (10h às 12h)"),
        ("turma2", "Turma 2 (14h às 16h)")
    )
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    matricula = models.CharField(max_length=10, verbose_name='Matrícula')
    secretaria = models.CharField(max_length=250)
    setor = models.CharField(max_length=250)
    celular = models.CharField(max_length=15, verbose_name='Celular')
    turma = models.CharField(max_length=10, choices=TURMAS)
    dt_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.turma}'

class PadronizacaoPagamentoInscricao(models.Model):
    TURMAS = (
        ("turma1", "Turma 1 (10h às 12h)"),
        ("turma2", "Turma 2 (14h às 16h)")
    )
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    matricula = models.CharField(max_length=10, verbose_name='Matrícula')
    secretaria = models.CharField(max_length=250)
    setor = models.CharField(max_length=250)
    celular = models.CharField(max_length=15, verbose_name='Celular')
    turma = models.CharField(max_length=10, choices=TURMAS)
    dt_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.turma}'

