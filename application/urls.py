from django.urls import re_path

from application import views


urlpatterns = [
    re_path("^new/$", views.postdoc, name="postdoc"),
]
