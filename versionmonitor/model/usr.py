from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

__author__ = 'Semyon'


@python_2_unicode_compatible
class ApiUser(models.Model):

    key = models.CharField(name="key", max_length=25, null=False, blank=False)

    push_id = models.CharField(name="push_id", max_length=25, null=False, blank=False)

    user = models.ForeignKey(User, related_name="+", null=False, blank=False)

    def __str__(self):
       return self.user.username + '@' + self.push_id