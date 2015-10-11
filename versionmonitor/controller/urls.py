from django.conf.urls import include, url
from versionmonitor.controller import project_controller

__author__ = 'dsv'


urlpatterns = [
    url(r'^$', project_controller.index, name='index'),
    url(r'^(?P<project_id>[0-9]+)$', project_controller.project_details, name='project_details'),
    url(r'^test$', project_controller.test, name='test'),
    url(r'^(?P<project_id>[0-9]+)/(?P<version_integer>[0-9]+)/icon$', project_controller.version_icon, name='version_icon')
]
