from django.contrib import admin
from .models import ApacheAccessLog

# Register your models here.
@admin.register(ApacheAccessLog)
class ApacheAccessLogAdmin(admin.ModelAdmin):
    list_display = ("ip", "timestamp", "method", "url", "status", "size")
    search_fields = ("ip", "url", "status")
    list_filter = ("status", "method", "protocol")