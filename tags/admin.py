from django.contrib import admin
from tags.models import Tag


# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = ('value',)

admin.site.register(Tag, TagAdmin)
