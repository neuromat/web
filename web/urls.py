from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import set_language

from mezzanine.conf import settings

# Uncomment to use blog as home page. See also urlpatterns section below.
from mezzanine.blog import views as blog_views
from application.views import category_page

# Trailing slahes for urlpatterns based on setup.
_slash = "/" if settings.APPEND_SLASH else ""

admin.autodiscover()

# urlpatterns = i18n_patterns(
#     # Change the admin prefix here to use an alternate URL for the
#     # admin interface, which would be marginally more secure.
#     url("^admin/", include(admin.site.urls)),
# )

urlpatterns = [
    url("^admin/", include(admin.site.urls)),
]

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

urlpatterns += [
    url("^$", blog_views.blog_post_list, name="home"),
    url("^newsletter/", include('newsletter.urls')),
    url("^postdoc/", include('application.urls')),
    url("^", include("mezzanine.urls")),
    url(r"^content/category/(?P<category>.*)%s$" % _slash, category_page, name="category_page"),
]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"

