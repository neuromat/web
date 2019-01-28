from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Postdoc, PostdocFile, Research


class ResearchInline(admin.StackedInline):
    model = Research
    extra = 1


class PostdocFileInline(admin.StackedInline):
    model = PostdocFile
    extra = 1
    verbose_name_plural = _('Files')


class PostdocAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['name', 'email', 'cpf', 'passport', 'phone', 'mobile_phone']
        }),
    )
    inlines = [ResearchInline, PostdocFileInline]
    search_fields = ['name']
    list_display = ('name', 'email', 'date')
    list_display_links = ('name', )

admin.site.register(Postdoc, PostdocAdmin)
