from django.contrib import admin

from .models import Newsletter, Subscription, FacebookHighlight


class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['email', 'create_date', 'status', 'status_date']
    list_display = ('email', 'create_date', 'status', 'status_date')
    search_fields = ['email']
    list_display_links = ('email',)

admin.site.register(Subscription, SubscriptionAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    fields = ['number', 'date', 'featured', 'publication', 'in_the_media', 'opportunity', 'streaming', 'event']
    list_display = ('number', 'date')
    search_fields = ['number']
    list_display_links = ('number',)
    ordering = ('-number',)

admin.site.register(Newsletter, NewsletterAdmin)


class FacebookHighlightAdmin(admin.ModelAdmin):
    fields = ['newsletter', 'text', 'image', 'image_url', 'facebook_link', 'date']
    list_display = ('newsletter', 'text', 'date')
    search_fields = ['text', 'newsletter__number']
    list_display_links = ('text',)
    ordering = ('-newsletter__number', 'date')

admin.site.register(FacebookHighlight, FacebookHighlightAdmin)
