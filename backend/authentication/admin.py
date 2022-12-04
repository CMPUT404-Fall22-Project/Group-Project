from django.contrib import admin
from .models import ExternalNode


class ExternalNodeAdmin(admin.ModelAdmin):
    list_display = ['host', 'api', 'authorization']
    ordering = ['host']


# Register your models here.
admin.site.register(ExternalNode, ExternalNodeAdmin)