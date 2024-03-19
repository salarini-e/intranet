from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

# Create your models here.
class Tipo(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Nome do Serviço', blank=True)
    sigla = models.CharField(max_length=3, verbose_name="Sigla", blank=True)
    descricao = models.TextField(default='')
    
    def __str__(self):
        return self.nome
    
class Secretaria(models.Model):
    nome = models.CharField(max_length=70)

    def total_chamados(self):
        chamados_por_tipo = Chamado.objects.filter(secretaria=self).values('tipo__nome').annotate(total=Count('tipo')).order_by('tipo')
        return chamados_por_tipo

    def __str__(self):
        return self.nome

class Setor(models.Model):
    secretaria = models.ForeignKey(Secretaria, verbose_name="Secretaria", on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='')
    cep = models.CharField(max_length=8, default='')
    bairro = models.CharField(max_length=50, default='')
    logradouro = models.CharField(max_length=150, default='')

    def total_chamados(self):
        chamados_por_tipo = Chamado.objects.filter(setor=self).values('tipo__nome').annotate(total=Count('tipo')).order_by('tipo')
        return chamados_por_tipo
    
    def __str__(self):
        return self.nome
    
class Servidor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=75)
    contato = models.CharField(max_length=11, default='Telefone')
    email = models.EmailField(max_length=254, default='')
    matricula = models.CharField(max_length=6, default='')
    setor = models.ForeignKey(Setor, verbose_name='Setor', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Atendente(Servidor):
    tipo = models.ManyToManyField(Tipo, verbose_name='Tipo')    
    
class Chamado(models.Model):
    
    prioridadeChoices = (
        ('0', 'Baixa'),
        ('1', 'Média'),
        ('2', 'Alta')
    )
    
    statusChoices = (
        ('0', 'Aberto'),
        ('1', 'Pendente'),
        ('2', 'Finalizado'),
    )
    
    secretaria = models.ForeignKey(Secretaria, verbose_name='Secretaria', on_delete=models.CASCADE, null=True)
    setor = models.ForeignKey(Setor, verbose_name='Setor', on_delete=models.CASCADE, null=True)
    contato = models.CharField(max_length=11, default='Telefone')
    requisitante = models.ForeignKey(Servidor, on_delete=models.CASCADE, related_name='requisitante')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=150)
    prioridade = models.CharField(max_length=1, choices=prioridadeChoices, default='0')
    status = models.CharField(max_length=1, choices=statusChoices, default='0')
    descricao = models.TextField(default='')
    atendente = models.ForeignKey(Atendente, verbose_name='Atendente', on_delete=models.CASCADE, related_name='atendente', null=True, default=None)
    dataAbertura = models.DateTimeField(auto_now_add=True)
    dataFechamento = models.DateTimeField(null=True, blank=False)
    numero = models.CharField(max_length=10, default=0)
    anexo = models.ImageField(upload_to='images', default=None, null=True, blank=True)
    
    
    def setNumero(self):
        ultimoChamado = Chamado.objects.last()
        if ultimoChamado:
            self.numero = str((int(ultimoChamado.numero) + 1)).zfill(5)
        else:
            self.numero = '00001'
        self.save()

    def notificaAtendente(self):
        atendentes = Atendente.objects.filter(tipo=self.tipo)
        emailList = []
        for atendente in atendentes:
            emailList.append(atendente.user.email)
            
        
        send_mail(
            'Um Novo Chamado foi aberto!',
            'Requisitante de nome ' + str(self.requisitante) + '\nNúmero do chamado: ' + self.numero + '\nCom o tipo: ' + str(self.tipo) + '\nNa data: ' + str(self.dataAbertura.strftime('%d/%m/%y')) + '\nAbriu um chamado com o assunto: ' + self.assunto + '\nE descrição: ' + self.descricao + '\nVeja os detalhes em: ' + '\nhttp://localhost:8000/chamado/' + str(self.id),
            "sebsecretaria.ti@gmail.com",
            emailList,
            fail_silently=False,
        )
        
            
        return None

class Comentario(models.Model):
    chamado = models.ForeignKey(Chamado, verbose_name='Chamado', on_delete=models.CASCADE)
    quemComentou = models.ForeignKey(Servidor, verbose_name='quemComentou', on_delete=models.CASCADE)
    dataHora = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(default='')
    confidencial = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.chamado} - {self.texto}'
    
    def notificaEnvolvidos(self):

        atendente = self.chamado.atendente
        requisitante = self.chamado.requisitante            
        emailList = []
        
        if atendente:
            emailList.append(atendente.user.email)
        if self.confidencial == False:
            emailList.append(requisitante.user.email)
        
        send_mail(
            'Há um novo comentário no seu chamado!',
            self.quemComentou.nome + ":\n" + self.texto + "\nhttp://intranet.novafriburgo.rj.gov.br/chamado/" + str(self.chamado.id),
            "sebsecretaria.ti@gmail.com",
            emailList,
            fail_silently=False,
        )
        
            
        return None    
    
class OSInternet(Chamado):
    nofcip = models.CharField(max_length=8)
    
class OSImpressora(Chamado):
    serie = models.CharField(max_length=8)
    contador = models.PositiveIntegerField()
    
class OSSistema(Chamado):
    sistema = models.CharField(max_length=50)
