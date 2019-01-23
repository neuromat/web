from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Postdoc, Research


class ResearchInline(admin.StackedInline):
    model = Research
    extra = 1
    verbose_name = _('Research')


class PostdocAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['name', 'email', 'cpf', 'passport', 'phone', 'mobile_phone']
        }),
    )
    inlines = [ResearchInline]
    search_fields = ['name']
    list_display = ('name', 'email', 'date')
    list_display_links = ('name', )

admin.site.register(Postdoc, PostdocAdmin)
