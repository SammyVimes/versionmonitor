"""versionmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from versionmonitor.controller import urls
from versionmonitor.controller import api_urls


def logout_fn(request):
    user = request.user
    if user and user.is_authenticated():
        logout(request)
    return redirect('/versionmonitor/login/')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^versionmonitor/logout/$', logout_fn, name="logout"),
    url(r'^versionmonitor/', include('registration.backends.simple.urls')),
    url(r'^versionmonitor/project/', include(urls)),
    url(r'^versionmonitor/api/', include(api_urls))
]
