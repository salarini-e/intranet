from django.contrib import admin
from .models import Ramal, Telefonista

class RamalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'secretaria', 'setor', 'referencia', 'responsavel', 'dt_inclusao')
    list_filter = ('secretaria', 'setor', 'responsavel')
    search_fields = ('numero', 'referencia', 'responsavel')
    list_per_page = 20

admin.site.register(Ramal, RamalAdmin)

class TelefonistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dt_inclusao', 'user_inclusao')
    search_fields = ('nome',)
    list_per_page = 20

admin.site.register(Telefonista, TelefonistaAdmin)