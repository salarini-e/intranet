from django.contrib import admin
from .models import Secretaria, Setor

@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'dt_inclusao')
    search_fields = ('nome', 'sigla')
    list_filter = ('dt_inclusao',)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'secretaria', 'dt_inclusao')
    search_fields = ('nome', 'sigla', 'secretaria__nome')
    list_filter = ('dt_inclusao',)
    autocomplete_fields = ['secretaria']