from django.contrib import admin
from .models import Pessoa

# Register your models here.
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'telefone', 'dt_nascimento', 'bairro', 'endereco', 'numero', 'complemento', 'cep', 'dt_inclusao')
    search_fields = ('nome', 'email', 'cpf')
    list_per_page = 20

admin.site.register(Pessoa, PessoaAdmin)