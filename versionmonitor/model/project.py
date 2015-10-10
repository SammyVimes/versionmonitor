from django.contrib.auth.models import User
from django.db import models
from versionmonitor.model.application import Application

__author__ = 'dsv'


class Project(models.Model):
    application = models.ForeignKey(Application, related_name="project", null=False, blank=False)

    projectName = models.CharField(name="project_name", max_length=50, null=False, blank=False)

    definition = models.TextField(name="definition", null=False, blank=False)


class ProjectMember(models.Model):

    MEMBER_ROLES = (
        ('A', 'Admin'),
        ('N', 'Normal'),
    )

    project = models.ForeignKey(Project, related_name="+", null=False, blank=False)

    user = models.ForeignKey(User)

    role = models.CharField(max_length=1, choices=MEMBER_ROLES)
