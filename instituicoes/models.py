from django.db import models
from django.contrib.auth.models import User

class Secretaria(models.Model):
   
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Secretaria'
        verbose_name_plural = 'Secretarias'
    
    nome=models.CharField(max_length=164, verbose_name='Nome')
    apelido=models.CharField(max_length=62, verbose_name='Apelido')
    sigla=models.CharField(max_length=8, verbose_name='Sigla')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao=models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True)

    def get_total_setores(self):        
        return Setor.objects.filter(secretaria = self).count()

class Setor(models.Model):
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
    
    nome=models.CharField(max_length=64, verbose_name='Nome')
    apelido=models.CharField(max_length=32, verbose_name='Apelido')
    sigla=models.CharField(max_length=8, verbose_name='Sigla')
    cep=models.CharField(max_length=10, verbose_name='CEP')
    bairro=models.CharField(max_length=64, verbose_name='Bairro')
    endereco=models.CharField(max_length=128, verbose_name='Endereço')
    secretaria=models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretaria', null=True)
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao=models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True)

    def get_total_servidores(self):
        return Servidor.objects.filter(setor = self).count()
    
class Servidor(models.Model):
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'
    
    user=models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True)
    nome=models.CharField(max_length=64, verbose_name='Nome')    
    cpf=models.CharField(max_length=14, verbose_name='CPF')    
    dt_nascimento=models.DateField(verbose_name='Data de nascimento')
    matricula=models.CharField(max_length=14, verbose_name='Matrícula', unique=True)
    telefone=models.CharField(max_length=15, verbose_name='Telefone')
    email=models.EmailField(max_length=64, verbose_name='E-mail')
    setor=models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
    avatar=models.ImageField(upload_to='avatars/', null=True, blank=True)
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao=models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True, related_name='servidor_user_inclusao')
    ativo  = models.BooleanField(default=True)
    