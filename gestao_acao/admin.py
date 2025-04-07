from django.contrib import admin

# Register your models here.
from .models import PlanejamentoAcao, Responsavel

admin.site.register(PlanejamentoAcao)
admin.site.register(Responsavel)