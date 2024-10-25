from django.contrib import admin
from .models import Topico, Subtopico, Arquivo_GoogleDrive
from .models import Arquivo_Texto, Arquivo_PDF

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

class ArquivoTextoAdmin(admin.ModelAdmin):
    list_display = ('subtopico', 'texto') 
    search_fields = ('subtopico__nome', 'texto')
    list_filter = ('subtopico',)
    ordering = ('subtopico',) 
admin.site.register(Arquivo_Texto, ArquivoTextoAdmin)

@admin.register(Arquivo_PDF)
class ArquivoPDFAdmin(admin.ModelAdmin):
    list_display = ('texto', 'subtopico', 'arquivo_pdf')
    search_fields = ('texto',) 
    list_filter = ('subtopico',)
    ordering = ('-id',)

    def has_add_permission(self, request):
        return True 

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True