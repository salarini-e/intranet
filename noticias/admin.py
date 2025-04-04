from django.contrib import admin
from .models import (Carrousell, Noticias, Imagens)
# Register your models here.

class CarrousellAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data')
    search_fields = ('titulo', 'data')
    ordering = ('-data', 'titulo')

admin.site.register(Carrousell, CarrousellAdmin)

class NoticiasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'dt_inclusao')
    search_fields = ('titulo', 'dt_inclusao')
    ordering = ('-dt_inclusao', 'titulo')

admin.site.register(Noticias, NoticiasAdmin)

class ImagensAdmin(admin.ModelAdmin):
    list_display = ('identificacao',)
    search_fields = ('identificacao',)
    ordering = ('identificacao',)
admin.site.register(Imagens, ImagensAdmin)