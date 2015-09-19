from django.conf.urls import include, url

urlpatterns = [
    url('^$', 'profilemaker.views.main'),
    url('^download/$', 'profilemaker.views.download'),
]
