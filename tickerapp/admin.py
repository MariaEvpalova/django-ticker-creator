from django.contrib import admin
from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('text', 'ip_address', 'user_agent', 'timestamp')
    search_fields = ('text', 'ip_address', 'user_agent')

admin.site.register(Request, RequestAdmin)
