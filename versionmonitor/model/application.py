from django.db import models

__author__ = 'dsv'


class Application(models.Model):
    package_name = models.CharField(name="package_name", max_length=25, null=False)

    application_name = models.CharField(name="application_name", max_length=50, null=False)

    def get_package_name(self):
        return self.package_name

    def get_application_name(self):
        return self.application_name


class ApplicationVersion(models.Model):
    application = models.ForeignKey(Application, related_name="versions", null=False, blank=False)

    version_integer = models.IntegerField(name="version_integer")

    version_string = models.CharField(name="version_string", null=False, blank=False, max_length=10)

    changes = models.TextField()
