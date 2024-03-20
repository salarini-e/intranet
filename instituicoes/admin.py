from django.contrib import admin
from .models import Secretaria, Setor, Servidor

@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'apelido', 'sigla', 'dt_inclusao', 'user_inclusao')
    list_filter = ('dt_inclusao', 'user_inclusao')
    search_fields = ('nome', 'apelido', 'sigla')

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'apelido', 'sigla', 'cep', 'bairro', 'endereco', 'secretaria', 'dt_inclusao', 'user_inclusao')
    list_filter = ('dt_inclusao', 'user_inclusao', 'secretaria')
    search_fields = ('nome', 'apelido', 'sigla')

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'setor', 'dt_inclusao', 'user_inclusao', 'ativo')
    list_filter = ('dt_inclusao', 'user_inclusao', 'ativo', 'setor')
    search_fields = ('nome', 'cpf', 'matricula', 'telefone', 'email')
