from django.contrib import admin
from .models import Registro
from django_select2.forms import ModelSelect2Widget

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    # Configura os campos exibidos na lista de registros
    list_display = ('nome', 'matricula', 'secretaria', 'setor', 'data_registro', 'entrada1', 'saida1', 'entrada2', 'saida2')
    list_filter = ('data_registro', 'secretaria', 'setor')  # Filtros laterais para pesquisa
    search_fields = ('nome', 'matricula')  # Campos pesquisáveis
    ordering = ('-data_registro', 'nome')  # Ordenação padrão
    readonly_fields = ('matricula', 'nome')  # Campos somente leitura no formulário

    # Campos exibidos no formulário de detalhes de um registro
    fieldsets = (
        ('Informações do Servidor', {
            'fields': ('user', 'matricula', 'nome', 'secretaria', 'setor')
        }),
        ('Registro de Ponto', {
            'fields': ('data_registro', 'entrada1', 'saida1', 'entrada2', 'saida2')
        }),
    )

    # Personalize os formulários para incluir o widget pesquisável
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["widget"] = ModelSelect2Widget(
                model=db_field.related_model,
                search_fields=["username__icontains", "email__icontains", "first_name__icontains", "last_name__icontains"],
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)