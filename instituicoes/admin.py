from django.contrib import admin
from .models import Secretaria, Setor, Servidor, Meta_Servidores, Dict_Mapeamento_Secretarias, Log_Nao_Encontrados

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
    autocomplete_fields = ('secretaria',)

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'setor', 'dt_inclusao', 'user_inclusao', 'ativo')
    list_filter = ('dt_inclusao', 'user_inclusao', 'ativo', 'setor')
    search_fields = ('nome', 'cpf', 'matricula', 'telefone', 'email')
    autocomplete_fields = ('user', 'user_inclusao', 'setor')

@admin.register(Meta_Servidores)
class MetaServidoresAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'secretaria', 'cpf', 'dt_inclusao')
    search_fields = ['nome', 'matricula', 'secretaria', 'cpf']
    readonly_fields = ('dt_inclusao',)

@admin.register(Dict_Mapeamento_Secretarias)
class DictMapeamentoSecretariasAdmin(admin.ModelAdmin):
    list_display = ('nome_portal', 'secretaria')
    search_fields = ('nome_portal', 'secretaria__nome')
    autocomplete_fields = ('secretaria',)

@admin.register(Log_Nao_Encontrados)
class LogNaoEncontradosAdmin(admin.ModelAdmin): 
    list_display = ('matricula', 'nome', 'secretaria')