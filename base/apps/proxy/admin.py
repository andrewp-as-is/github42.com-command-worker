from django.contrib import admin

from .models import Proxy

class ProxyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'addr',
        'is_active',
        'is_http',
        'is_socks4',
        'calls_count',
        'errors_count',
    ]
    list_filter = ['is_active','is_http','is_socks4',]

admin.site.register(Proxy,ProxyAdmin)
