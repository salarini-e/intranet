from django.contrib import admin
from .models import Registro, Responsavel, Acesso

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    # Configura os campos exibidos na lista de registros
    list_display = ('nome', 'matricula', 'secretaria', 'setor', 'data_registro', 'entrada1', 'saida1', 'entrada2', 'saida2', 'ip_inclusao')
    list_filter = ('data_registro', 'secretaria', 'setor')  # Filtros laterais para pesquisa
    search_fields = ('nome', 'matricula')  # Campos pesquisáveis
    ordering = ('-data_registro', 'nome')  # Ordenação padrão
    # readonly_fields = ('matricula', 'nome', 'ip_inclusao')  # Campos somente leitura no formulário

    # Campos exibidos no formulário de detalhes de um registro
    fieldsets = (
        ('Informações do Servidor', {
            'fields': ('user', 'matricula', 'nome', 'secretaria', 'setor', 'ip_inclusao')
        }),
        ('Registro de Ponto', {
            'fields': ('data_registro', 'entrada1', 'saida1', 'entrada2', 'saida2')
        }),
    )

    autocomplete_fields = ('user',)


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    # Configuração de exibição na lista de registros
    list_display = ('user', 'geral', 'secretaria', 'setor', 'dt_inclusao')
    list_filter = ('geral', 'secretaria', 'setor', 'dt_inclusao')  # Filtros laterais
    search_fields = ('user__username', 'user__email', 'secretaria__nome', 'setor__nome')  # Campos pesquisáveis
    ordering = ('-dt_inclusao', 'user__username')  # Ordenação padrão

    # Configuração dos campos no formulário de detalhes
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'geral', 'pode_alterar_registro')
        }),
        ('Vinculação', {
            'fields': ('secretaria', 'setor')
        }),
        ('Outros', {
            'fields': ('dt_inclusao',),
            'classes': ('collapse',),  # Deixa essa seção colapsável
        }),
    )

    # Torna o campo de data somente leitura
    readonly_fields = ('dt_inclusao',)

    # Torna o campo `user` uma barra de pesquisa
    autocomplete_fields = ('user', 'secretaria', 'setor')

@admin.register(Acesso)
class AcessoAdmin(admin.ModelAdmin):
    list_display = ( 'tipo', 'secretaria', 'setor', 'servidor')