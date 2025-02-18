from django.contrib import admin
from .models import Projetos, Fases, Categorias, Prioridade, Tarefas, Atividades, Comentarios, Grupo, Anexo

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user_inclusao', 'dt_inclusao', 'dt_att')
    search_fields = ('nome',)
    readonly_fields = ('dt_inclusao', 'dt_att')

@admin.register(Projetos)
class ProjetosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'data_inicio', 'data_fim', 'user_inclusao', 'dt_inclusao', 'dt_att')
    list_filter = ('status', 'dt_inclusao', 'dt_att')
    search_fields = ('nome', 'descricao')
    ordering = ('data_inicio',)
    readonly_fields = ('dt_inclusao', 'dt_att')


@admin.register(Fases)
class FasesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'projeto', 'ordem', 'status', 'data_inicio', 'data_fim', 'user_inclusao', 'dt_inclusao', 'dt_att')
    list_filter = ('status', 'dt_inclusao', 'dt_att')
    search_fields = ('nome', 'descricao', 'projeto__nome')
    ordering = ('ordem',)
    readonly_fields = ('dt_inclusao', 'dt_att')


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'user_inclusao', 'dt_inclusao', 'dt_att')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('dt_inclusao', 'dt_att')


@admin.register(Prioridade)
class PrioridadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor', 'descricao')
    search_fields = ('nome',)


@admin.register(Tarefas)
class TarefasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fase', 'orderm', 'concluido', 'prioridade', 'user_inclusao', 'dt_inclusao', 'dt_att')
    list_filter = ('concluido', 'prioridade', 'dt_inclusao', 'dt_att')
    search_fields = ('nome', 'descricao', 'fase__nome', 'fase__projeto__nome')
    ordering = ('orderm',)
    readonly_fields = ('dt_inclusao', 'dt_att')


@admin.register(Atividades)
class AtividadesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tarefa', 'ordem', 'concluido', 'data_execucao', 'user_inclusao', 'dt_inclusao', 'dt_att')
    list_filter = ('concluido', 'dt_inclusao', 'dt_att')
    search_fields = ('nome', 'descricao', 'tarefa__nome', 'tarefa__fase__nome', 'tarefa__fase__projeto__nome')
    ordering = ('ordem',)
    readonly_fields = ('dt_inclusao', 'dt_att')


@admin.register(Comentarios)
class ComentariosAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'atribuicao', 'tarefa', 'atividade', 'user_inclusao', 'dt_inclusao', 'dt_att')
    list_filter = ('atribuicao', 'dt_inclusao', 'dt_att')
    search_fields = ('descricao', 'tarefa__nome', 'atividade__nome')
    readonly_fields = ('dt_inclusao', 'dt_att')

@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ('arquivo', 'tarefa')        
    search_fields = ('descricao', 'tarefa__nome')        