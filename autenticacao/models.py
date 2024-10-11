#Importações das estruturas padrões do Django.
from django.db import models
from django.contrib.auth.models import User

class Pessoa(models.Model):
    def __str__(self):
        return '%s - Email: %s' % (self.nome, self.email)
    
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    nome=models.CharField(max_length=64, verbose_name='Nome')
    email=models.EmailField()
    cpf=models.CharField(max_length=14, verbose_name='CPF', unique=True, null=True)
    telefone=models.CharField(max_length=15, verbose_name='Telefone', null=True)
    dt_nascimento=models.DateField(verbose_name='Data de nascimento', null=True)
    bairro=models.CharField(max_length=64, verbose_name='Bairro', null=True)
    endereco=models.CharField(max_length=128, verbose_name='Endereço', null=True)
    numero=models.CharField(max_length=8, verbose_name='Número', null=True)
    complemento=models.CharField(max_length=128, verbose_name='Complemento', blank=True, null=True)
    cep = models.CharField(max_length=9, verbose_name='CEP', null=True)
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    possui_cnpj=models.BooleanField(default=False, verbose_name='Você possui empresa?')

    def save(self, *args, **kwargs):
        if not self.user.first_name == self.nome:
            self.user.first_name = self.nome
        if not self.user.email == self.email:
            self.user.email = self.email
        self.user.save()
        super().save(*args, **kwargs)