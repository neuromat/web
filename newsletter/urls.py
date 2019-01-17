from django.conf.urls import url

from newsletter import views

urlpatterns = [
    url(r'^subscription', views.subscription, name='subscription'),
    url(r'^previous', views.previous_issues, name='previous_issues'),
    url(r'^(?P<newsletter_number>\d+)$', views.newsletter, name='newsletter'),
]
