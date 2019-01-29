from django.contrib import admin

from .models import Newsletter, Subscription, FacebookHighlight


admin.site.register(Newsletter)
admin.site.register(FacebookHighlight)


class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['email', 'create_date', 'status', 'status_date']
    list_display = ('email', 'create_date', 'status', 'status_date')
    search_fields = ['email']
    list_display_links = ('email',)

admin.site.register(Subscription, SubscriptionAdmin)
