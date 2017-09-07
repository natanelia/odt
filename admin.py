from django.contrib import admin

from .models import Reference

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('key_label', 'key', 'value', 'value_label')

admin.site.register(Reference, ReferenceAdmin)