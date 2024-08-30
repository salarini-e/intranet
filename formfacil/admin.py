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
    # Campos que serão exibidos na lista de registros
    list_display = ('nome', 'matricula', 'secretaria', 'setor', 'telefone', 'turma_escolhida', 'dt_registro')
    
    # Campos pelos quais você pode buscar
    search_fields = ('nome', 'matricula', 'telefone', 'secretaria', 'setor')
    
    # Filtros laterais para facilitar a busca
    list_filter = ('turma_escolhida')
    
    # Ordem padrão dos registros
    ordering = ('-dt_registro', 'nome')  # Exibe os registros mais recentes primeiro

# Registro do modelo no admin
admin.site.register(Cadastro_Aulas_Processo_Digital, CadastroAulasProcessoDigitalAdmin)