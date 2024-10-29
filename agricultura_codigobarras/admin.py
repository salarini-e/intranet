from django.contrib import admin
from .models import Equipamento, User_Agricultura

class UserAgriculturaAdmin(admin.ModelAdmin):
    search_fields = ['servidor__nome', 'servidor__cpf', 'servidor__matricula']

admin.site.register(User_Agricultura, UserAgriculturaAdmin)
admin.site.register(Equipamento)