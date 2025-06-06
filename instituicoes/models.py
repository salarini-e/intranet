from django.db import models
from django.contrib.auth.models import User
import os

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
    cpf=models.CharField(max_length=14, verbose_name='CPF', unique=True)    
    dt_nascimento=models.DateField(verbose_name='Data de nascimento')
    matricula=models.CharField(max_length=50, verbose_name='Matrícula', unique=True)
    telefone=models.CharField(max_length=15, verbose_name='Telefone')
    email=models.EmailField(max_length=64, verbose_name='E-mail')
    setor=models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
    avatar=models.ImageField(upload_to='avatars/', null=True, blank=True)
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao=models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', blank=True, null=True, related_name='servidor_user_inclusao')
    ativo  = models.BooleanField(default=True)

    
    def save(self, *args, **kwargs):
        # Verifique se houve uma alteração no avatar
        if self.pk:  # Se o objeto já existe no banco de dados
            try:
                servidor = Servidor.objects.get(pk=self.pk)
                
                if servidor.avatar and self.avatar and self.avatar != servidor.avatar:  # Se houver um novo avatar
                    if os.path.isfile(servidor.avatar.path):  # Verifique se o arquivo antigo existe
                        os.remove(servidor.avatar.path)  # Exclua o arquivo antigo
            except Servidor.DoesNotExist:
                pass  # Se não houver objeto anterior, apenas passe
        super().save(*args, **kwargs)
    
    def get_avatar(self):
         return self.avatar.url if self.avatar else '/static/images/user.png'
            
        
class Meta_Servidores(models.Model):
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Meta-servidor'
        verbose_name_plural = 'Meta-servidores (Lista de servidores do site da prefeitura)'
    
    nome=models.CharField(max_length=164, verbose_name='Nome')    
    matricula=models.CharField(max_length=14, verbose_name='Matrícula', unique=True)
    secretaria = models.CharField(max_length=164, verbose_name='Secretaria')    
    cpf=models.CharField(max_length=14, verbose_name='Parte do CPF')    
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

class Dict_Mapeamento_Secretarias(models.Model):
    def __str__(self):
        return f'{self.nome_portal} - {self.nome_intranet}'
    
    class Meta:
        verbose_name = 'Dicionário de secretarias Portal x Intranet'
        verbose_name_plural = 'Dicionário de secretarias Portal x Intranet'

    nome_portal = models.CharField(max_length=164, verbose_name='Nome')
    nome_intranet = models.CharField(max_length=164, verbose_name='Nome Intranet')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretaria', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.secretaria:
            secretaria = Secretaria.objects.filter(nome=self.nome_portal)
            if secretaria.exists():
                self.secretaria = secretaria.first()
        else:            
            raise ValueError("O nome da secretaria não corresponde com as cadastradas na Intranet.")

        super().save(*args, **kwargs)
    
   