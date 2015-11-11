from django import template
from datetime import datetime
__author__ = 'Semyon'


register = template.Library()


@register.simple_tag
def project_last_version(project):
    versions = project.application.versions.all()
    last_version = -1
    v_count = versions.count()
    if v_count > 0:
        last_version = versions[v_count - 1].version_integer
    return last_version


@register.simple_tag
def project_last_version_string(project):
    versions = project.application.versions.all()
    last_version = "not uploaded"
    v_count = versions.count()
    if v_count > 0:
        last_version = versions[v_count - 1].version_string
    return last_version

@register.simple_tag
def project_last_version_date(project):
    versions = project.application.versions.all()
    last_version = datetime.now()
    v_count = versions.count()
    if v_count > 0:
        last_version = versions[v_count - 1].version_date
    return last_version

@register.simple_tag
def project_last_version_date_string(project):
    versions = project.application.versions.all()
    last_version = datetime.now()
    v_count = versions.count()
    if v_count > 0:
        last_version = versions[v_count - 1].version_date
    return format_date(last_version)

@register.simple_tag
def format_date(d):
    s = d.strftime("%d.%m.%Y %H:%M")
    return s