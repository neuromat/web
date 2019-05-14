from django.conf.urls import url

from application import views


urlpatterns = [
    url("^new/$", views.postdoc, name="postdoc"),
]
