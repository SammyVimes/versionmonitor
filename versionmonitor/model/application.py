from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

__author__ = 'dsv'


@python_2_unicode_compatible
class Application(models.Model):
    package_name = models.CharField(name="package_name", max_length=50, null=False)

    application_name = models.CharField(name="application_name", max_length=50, null=False)

    def get_package_name(self):
        return self.package_name

    def get_application_name(self):
        return self.application_name

    def __str__(self):
       return self.application_name + '(' + self.package_name + ')'


@python_2_unicode_compatible
class ApplicationVersion(models.Model):
    application = models.ForeignKey(Application, related_name="versions", null=False, blank=False)

    version_integer = models.IntegerField(name="version_integer")

    version_string = models.CharField(name="version_string", null=False, blank=False, max_length=10)

    changes = models.TextField()

    def __str__(self):
       return self.application.application_name + '(' + self.version_string + ')'
