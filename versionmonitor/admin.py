from django.contrib import admin
from versionmonitor import models

__author__ = 'dsv'

admin.site.register(models.Project)
admin.site.register(models.ProjectMember)
admin.site.register(models.Application)
admin.site.register(models.ApplicationVersion)
