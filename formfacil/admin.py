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


class InscricaoDecretosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'secretaria', 'setor', 'telefone', 'horarios', 'dt_registro')
    list_filter = ('horarios', 'secretaria', 'setor')
    search_fields = ('nome', 'matricula', 'cpf')    
    ordering = ('-dt_registro', 'nome')

admin.site.register(Inscricao_Decretos_Portaria_E_Atos_Do_Prefeito, InscricaoDecretosAdmin)

class CadastroAlmoxarifadoAdmin(admin.ModelAdmin):
    list_display = ('nome_requisitante', 'matricula', 'cpf', 'secretaria', 'autorizador', 'responsavel_material', 'dt_registro')
    search_fields = ('nome_requisitante', 'matricula', 'cpf', 'secretaria', 'autorizador', 'responsavel_material')
    list_filter = ('secretaria',)
    ordering = ('-dt_registro', 'nome_requisitante')

admin.site.register(Cadastro_de_Almoxarifado, CadastroAlmoxarifadoAdmin)

class AvaliacaoSistemaELAdmin(admin.ModelAdmin):
    list_display = ('sistema', 'usuario_nome', 'usuario_matricula', 'satisfacao', 'houve_lentidao', 'sugestao', 'data_avaliacao', 'usuario_inclusao')
    search_fields = ('sistema', 'usuario_nome', 'usuario_matricula', 'sugestao')
    list_filter = ('sistema', 'satisfacao', 'houve_lentidao', 'data_avaliacao')
    ordering = ('-data_avaliacao', 'sistema')

admin.site.register(AvaliacaoSistemaEL, AvaliacaoSistemaELAdmin)

class SolicitacaoEmailInstitucionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cpf', 'secretaria', 'email_institucional', 'dt_registro')
    search_fields = ('nome', 'matricula', 'cpf', 'email_institucional', 'secretaria')
    list_filter = ('secretaria',)
    ordering = ('-dt_registro', 'nome')

admin.site.register(SolicitacaoEmailInstitucional, SolicitacaoEmailInstitucionalAdmin)

class ProcessoDigitalInscricaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'secretaria', 'setor', 'celular', 'turma', 'dt_inscricao')
    search_fields = ('nome', 'matricula', 'secretaria', 'setor', 'celular')
    list_filter = ('turma', 'secretaria', 'setor')
    ordering = ('-dt_inscricao', 'nome')

class PadronizacaoPagamentoInscricaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'secretaria', 'setor', 'celular', 'turma', 'dt_inscricao')
    search_fields = ('nome', 'matricula', 'secretaria', 'setor', 'celular')
    list_filter = ('turma', 'secretaria', 'setor')
    ordering = ('-dt_inscricao', 'nome')

admin.site.register(ProcessoDigitalInscricao, ProcessoDigitalInscricaoAdmin)
admin.site.register(PadronizacaoPagamentoInscricao, PadronizacaoPagamentoInscricaoAdmin)