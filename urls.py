from django.conf.urls import include, url
from profilemaker.views import main, download

urlpatterns = [
    url('^$', main, name="main"),
    url('^download/(?P<what>.*)$', download, name="download"),
]
