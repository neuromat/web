from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Postdoc, PostdocFile, Research, FeatureCard, SwiperCard, Banner, SocialMediaLink, NeuroCineMat
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost
from copy import deepcopy
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage


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
blog_fieldsets[0][1]["fields"].insert(-5, "legend")
blog_fieldsets[0][1]["fields"].insert(-6, "credits")


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(Banner, BannerAdmin)


class FeatureCardsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(FeatureCard, FeatureCardsAdmin)


class SwiperCardsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(SwiperCard, SwiperCardsAdmin)


class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'icon_class')


admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)

class NeuroCineMatAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_link')


admin.site.register(NeuroCineMat, NeuroCineMatAdmin)

class MyBlogPostAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets


admin.site.unregister(BlogPost)
admin.site.register(BlogPost, MyBlogPostAdmin)

pages_fieldsets = deepcopy(PageAdmin.fieldsets)
pages_fieldsets[0][1]["fields"].insert(-2, "page_image")
pages_fieldsets[0][1]["fields"].insert(-3, "content")


class CustomPageAdmin(PageAdmin):
    fieldsets = pages_fieldsets


admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, CustomPageAdmin)