from django.conf.urls import include, url

__author__ = 'dsv'


urlpatterns = [
    url(r'^versionmonitor/project/', include(urls))
]
