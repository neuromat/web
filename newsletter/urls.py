from django.urls import re_path

from newsletter import views

urlpatterns = [
    re_path("^subscription/$", views.subscription, name='subscription'),
    re_path("^unsubscription/$", views.unsubscription, name='unsubscription'),
    re_path("^previous/$", views.previous_issues, name='previous_issues'),
    re_path("^(?P<newsletter_number>\d+)/$", views.newsletter, name='newsletter'),
    re_path("^(?P<newsletter_number>\d+)/submit/$", views.send_newsletter, name='send_newsletter'),
]
