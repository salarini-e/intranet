from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TipoChamado, Atendente, Chamado, Mensagem, OSInternet, OSImpressora, OSSistemas, PeriodoPreferencial, Pausas_Execucao_do_Chamado, Historico_Designados, SubTipoChamado, chamadoSatisfacao

@admin.register(TipoChamado)
class TipoChamadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'descricao', 'dt_inclusao', 'user_inclusao')
    list_filter = ('dt_inclusao', 'user_inclusao')
    search_fields = ('nome', 'sigla')

@admin.register(Atendente)
class AtendenteAdmin(admin.ModelAdmin):
    list_display = ('servidor', 'nome_servidor', 'dt_inclusao', 'user_inclusao', 'ativo')
    list_filter = ('dt_inclusao', 'user_inclusao', 'ativo')
    search_fields = ('servidor__nome', 'nome_servidor')
    autocomplete_fields = ('servidor', 'user_inclusao')


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('n_protocolo', 'assunto','requisitante', 'profissional_designado', 'status',  'dt_inclusao', 'dt_execucao', 'dt_fechamento')
    list_filter = ('dt_inclusao', 'user_inclusao', 'dt_atualizacao', 'user_atualizacao', 'dt_execucao', 'dt_fechamento', 'prioridade', 'status')
    search_fields = ('setor__nome', 'telefone', 'requisitante__nome', 'assunto')

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'mensagem', 'dt_inclusao', 'user_inclusao', 'confidencial')
    list_filter = ('dt_inclusao', 'user_inclusao', 'confidencial')
    search_fields = ('chamado__assunto', 'servidor__nome', 'mensagem')

@admin.register(OSInternet)
class OSInternetAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'nofcip')

@admin.register(OSImpressora)
class OSImpressoraAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'n_serie', 'contador')

@admin.register(OSSistemas)
class OSSistemasAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'sistema')

@admin.register(PeriodoPreferencial)
class PeriodoPreferencialAdmin(admin.ModelAdmin):
    list_display = ('nome',)    
    search_fields = ('nome',)

@admin.register(Pausas_Execucao_do_Chamado)
class PausasExecucaoChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'chamado', 'dt_inicio', 'dt_fim', 'user_inclusao', 'user_fim')
    list_filter = ('dt_inicio', 'dt_fim')
    search_fields = ('chamado__n_protocolo',)


@admin.register(SubTipoChamado)
class SubTipoChamadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'dt_inclusao', 'user_inclusao')
    list_filter = ('dt_inclusao', 'user_inclusao')
    search_fields = ('nome', 'tipo__nome')

@admin.register(chamadoSatisfacao)
class chamadoSatisfacaoAdmin(admin.ModelAdmin):
    list_display = (
        'chamado', 
        'dt_inclusao'
    )
    list_filter = (
        'avaliacao', 
        'cordialidade', 
        'resolucao', 
        'receberia_novamente_o_tecnico', 
        'dt_inclusao'
    )
    search_fields = ('chamado__id', 'chamado__descricao', 'comentario')
    readonly_fields = ('dt_inclusao',)
