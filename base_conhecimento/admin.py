from django.contrib import admin
from .models import Topico, Subtopico, Arquivo_GoogleDrive

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dt_inclusao', 'user_inclusao')
    search_fields = ('nome', 'palavras_chave')
    list_filter = ('dt_inclusao', 'user_inclusao')
    date_hierarchy = 'dt_inclusao'
    ordering = ('-dt_inclusao',)

@admin.register(Subtopico)
class SubtopicoAdmin(admin.ModelAdmin):
    list_display = ('tema', 'tipo', 'dt_inclusao', 'user_inclusao', 'topico')
    search_fields = ('tema',)
    list_filter = ('tipo', 'dt_inclusao', 'user_inclusao', 'topico')
    date_hierarchy = 'dt_inclusao'
    ordering = ('-dt_inclusao',)

@admin.register(Arquivo_GoogleDrive)
class Arquivo_GoogleDriveAdmin(admin.ModelAdmin):
    list_display = ('subtopico', 'iframe')
    search_fields = ('subtopico__tema',)
    list_filter = ('subtopico',)
