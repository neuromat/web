from django.contrib import admin

from .models import Newsletter, Subscription, FacebookHighlight


admin.site.register(Newsletter)
admin.site.register(Subscription)
admin.site.register(FacebookHighlight)
