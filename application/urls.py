from django.conf.urls import url

from application import views


urlpatterns = [
    url(r'^new', views.postdoc, name="postdoc"),
]
