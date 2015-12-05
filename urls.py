from django.conf.urls import include, url

urlpatterns = [
    url('^$', 'profilemaker.views.main'),
    url('^download/(?P<what>.*)$', 'profilemaker.views.download'),
]
