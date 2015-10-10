# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('package_name', models.CharField(max_length=25)),
                ('application_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('version_integer', models.IntegerField()),
                ('version_string', models.CharField(max_length=10)),
                ('changes', models.TextField()),
                ('application', models.ForeignKey(related_name='+', to='versionmonitor.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=50)),
                ('definition', models.TextField()),
                ('application', models.ForeignKey(related_name='project', to='versionmonitor.Application')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('A', 'Admin'), ('N', 'Normal')], max_length=1)),
                ('project', models.ForeignKey(related_name='+', to='versionmonitor.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
