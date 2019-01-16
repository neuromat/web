from django.conf.urls import url

from newsletter import views

urlpatterns = [
    url(r'^subscription', views.subscription, name='subscription'),
]
