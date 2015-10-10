from django.db import models

__author__ = 'dsv'


class Application(models.Model):
    packageName = models.CharField(name="package_name", max_length=25, null=False)

    applicationName = models.CharField(name="application_name", max_length=50, null=False)

    def get_package_name(self):
        return self.packageName

    def get_application_name(self):
        return self.applicationName


class ApplicationVersion(models.Model):
    application = models.ForeignKey(Application, related_name="+", null=False, blank=False)

    version = models.IntegerField(name="version_integer")

    versionString = models.CharField(name="version_string", null=False, blank=False, max_length=10)

    changes = models.TextField()
