from django.contrib import admin
from .models import Ramal

class RamalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'secretaria', 'setor', 'referencia', 'responsavel', 'dt_inclusao')
    list_filter = ('secretaria', 'setor', 'responsavel')
    search_fields = ('numero', 'referencia', 'responsavel')
    list_per_page = 20

admin.site.register(Ramal, RamalAdmin)