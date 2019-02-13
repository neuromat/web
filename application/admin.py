from copy import deepcopy
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Postdoc, PostdocFile, Research
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost


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

# add fields "hide_post" and "altmetric type/number" to blog subclasses in the admin
blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"] += ("hide_post", "altmetric_type", "altmetric_number")


class MyBlogPostAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets

admin.site.unregister(BlogPost)
admin.site.register(BlogPost, MyBlogPostAdmin)
