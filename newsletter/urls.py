from django.conf.urls import url

from newsletter import views

urlpatterns = [
    url("^subscription/$", views.subscription, name='subscription'),
    url("^unsubscription/$", views.unsubscription, name='unsubscription'),
    url("^previous/$", views.previous_issues, name='previous_issues'),
    url("^(?P<newsletter_number>\d+)/$", views.newsletter, name='newsletter'),
    url("^(?P<newsletter_number>\d+)/submit/$", views.send_newsletter, name='send_newsletter'),
]
