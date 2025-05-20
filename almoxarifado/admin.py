from django.contrib import admin

from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_total')
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 10
    list_editable = ('quantidade_total',)
    fieldsets = (
        (None, {
            'fields': ('nome', 'quantidade_total')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('nome', 'quantidade_total')
        }),
    )
