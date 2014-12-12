from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Stack, StackItem, Text, Media, Discussion, Poll

class StackItemInline(GenericStackedInline):
    model = StackItem

class StackItemAdmin(admin.ModelAdmin):
    inlines = [
        StackItemInline,
    ]

admin.site.register(Stack)
admin.site.register(StackItem, StackItemAdmin)
admin.site.register(Text)
admin.site.register(Media)
admin.site.register(Discussion)
admin.site.register(Poll)