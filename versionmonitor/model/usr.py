from django.contrib.auth.models import User
from django.db import models

__author__ = 'Semyon'


class ApiUser(models.Model):

    key = models.CharField(name="key", max_length=25, null=False, blank=False)

    user = models.ForeignKey(User, related_name="+", null=False, blank=False)
