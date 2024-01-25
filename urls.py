from django.urls import path, re_path
from profilemaker.views import download, main

urlpatterns = [
    path("", main, name="main"),
    re_path(r"^download/(?P<what>.*)$", download, name="download"),
]
