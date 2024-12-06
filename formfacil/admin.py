from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FormIndicacaoComitePSP)
admin.site.register(CadastroWebex)
admin.site.register(FormSugestaoSemanaNacionalCET2024)
admin.site.register(Sistemas_EL)
admin.site.register(CadastroEL)
admin.site.register(Opcao_Turmas)

class CadastroAulasProcessoDigitalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'secretaria', 'setor', 'telefone', 'turma_escolhida', 'dt_registro')
    search_fields = ('nome', 'matricula', 'telefone', 'secretaria', 'setor')
    list_filter = ('turma_escolhida',)
    ordering = ('-dt_registro', 'nome')  

admin.site.register(Cadastro_Aulas_Processo_Digital, CadastroAulasProcessoDigitalAdmin)


class CadastroAulasEmissoresAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cpf', 'secretaria', 'setor', 'telefone', 'dt_registro')
    search_fields = ('nome', 'matricula','cpf', 'telefone', 'secretaria', 'setor')
    list_filter = ('secretaria', 'setor')
    ordering = ('-dt_registro', 'nome')

class CadastroAulasContadoresAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cpf', 'secretaria', 'setor', 'telefone', 'dt_registro')
    search_fields = ('nome', 'matricula','cpf', 'telefone', 'secretaria', 'setor')
    list_filter = ('secretaria', 'setor')
    ordering = ('-dt_registro', 'nome')

admin.site.register(Cadastro_Aulas_Treinamento_Tributario_Emissores_Taxas, CadastroAulasEmissoresAdmin)
admin.site.register(Cadastro_Aulas_Treinamento_Tributario_Contadores, CadastroAulasContadoresAdmin)

class OpcaoTurmasDecretosAdmin(admin.ModelAdmin):
    list_display = ('dia_da_semana', 'dia_do_mes', 'hora_inicio', 'ativo', 'get_total')
    list_filter = ('ativo',)
    search_fields = ('dia_da_semana', 'dia_do_mes')
    list_per_page = 10
    readonly_fields = ('get_total',)

    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total de Inscrições'

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Opcao_Turmas_Decretos, OpcaoTurmasDecretosAdmin)

class InscricaoDecretosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'secretaria', 'setor', 'telefone', 'turma_escolhida', 'dt_registro')
    list_filter = ('turma_escolhida', 'secretaria', 'setor')
    search_fields = ('nome', 'matricula', 'cpf')
    list_per_page = 10
    ordering = ('dt_registro',)

admin.site.register(Inscricao_Decretos_Portaria_Atos_Prefeito, InscricaoDecretosAdmin)