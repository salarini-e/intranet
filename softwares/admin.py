from django.contrib import admin
from .models import TipoSistema, Sistemas, TipoDownload, Downloads

@admin.register(TipoSistema)
class TipoSistemaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(Sistemas)
class SistemasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'url', 'tipo', 'listar', 'dt_inclusao')
    list_filter = ('tipo', 'listar')
    search_fields = ('nome', 'descricao')

@admin.register(TipoDownload)
class TipoDownloadAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(Downloads)
class DownloadsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'arquivo', 'tamanho', 'tipo', 'dt_inclusao')
    list_filter = ('tipo',)
    search_fields = ('nome', 'descricao')

