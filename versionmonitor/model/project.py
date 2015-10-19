from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models
from versionmonitor.model.application import Application
from versionmonitor import config
from urllib import parse

__author__ = 'dsv'


@python_2_unicode_compatible
class Project(models.Model):
    application = models.ForeignKey(Application, related_name="project", null=False, blank=False)

    project_name = models.CharField(name="project_name", max_length=50, null=False, blank=False)

    definition = models.TextField(name="definition", null=False, blank=False)

    def __str__(self):
       return self.project_name


@python_2_unicode_compatible
class ProjectMember(models.Model):

    MEMBER_ROLES = (
        ('A', 'Admin'),
        ('N', 'Normal'),
    )

    def __str__(self):
       return self.user.username + '@' + self.project.project_name

    project = models.ForeignKey(Project, related_name="+", null=False, blank=False)

    user = models.ForeignKey(User, related_name="+", null=False, blank=False)

    role = models.CharField(max_length=1, choices=MEMBER_ROLES)

    def get_monogram(self):
        user = self.user
        first_name = user.first_name
        last_name = user.last_name
        f = "U"
        l = "U"
        if len(first_name) > 0:
            f = first_name[0]
        if len(last_name) > 0:
            l = last_name[0]
        url = config.MONOGRAM_URL.replace("${monogram}", (f + l))
        url = parse.quote(url)
        url = url.replace("%", "").replace("3A", ":")
        return url
