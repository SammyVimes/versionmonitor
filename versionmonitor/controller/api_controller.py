from tkinter import Image
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import simplejson as simplejson
from versionmonitor import config
from versionmonitor.model.project import Project, ProjectMember
from versionmonitor.templatetags import project_tags

__author__ = 'Semyon'


def project_to_dic(p):
    a = p.application
    last_version = project_tags.project_last_version(p)
    last_version_string = project_tags.project_last_version_string(p)
    jsonp = {
        'packageName': a.package_name,
        'name': p.project_name,
        'id': p.pk,
        'lastVersionString': last_version_string,
        'lastVersionInt': last_version,
        'definition': p.definition
    }
    return jsonp


def version_to_dic(v):
    jsonv = {
        'versionInteger': v.version_integer,
        'versionString': v.version_string,
        'changes': v.changes,
    }
    return jsonv


def index(request):
    all_projects = Project.objects.all()
    projects = []
    for p in all_projects:
        a = p.application
        last_version = project_tags.project_last_version(p)
        last_version_string = project_tags.project_last_version_string(p)
        jsonp = {
            'packageName': a.package_name,
            'name': p.project_name,
            'id': p.pk,
            'lastVersionString': last_version_string,
            'lastVersionInt': last_version,
            'definition': p.definition
        }
        projects.append(jsonp)
    return HttpResponse(simplejson.dumps(projects), content_type="application/json")


def project_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    versions = project.application.versions.all()
    versions = reversed(list(versions))
    proj_dic = project_to_dic(project)
    versions_dics = [version_to_dic(v) for v in versions]
    response = {
        'project': proj_dic,
        'versions': versions_dics
    }
    return HttpResponse(simplejson.dumps(response), content_type="application/json")


def get_apk(request, project_id, version_integer):
    if int(version_integer) < 0:
        return None
    project = Project.objects.get(pk=project_id)
    versions = project.application.versions
    version = versions.filter(version_integer=version_integer)[0]
    apk_uri = config.APPS_FOLDER + str(project.pk) + "\\" + str(version.version_integer) + "\\" + "app.apk"
    try:
        with open(apk_uri, "rb") as f:
            return HttpResponse(f.read(), content_type="application/vnd.android.package-archive")
    except IOError:
        return None


def version_icon(request, project_id, version_integer):
    if int(version_integer) < 0:
        return None
    project = Project.objects.get(pk=project_id)
    versions = project.application.versions
    version = versions.filter(version_integer=version_integer)[0]
    img_uri = config.APPS_FOLDER + str(project.pk) + "\\" + str(version.version_integer) + "\\" + "icon.png"
    try:
        with open(img_uri, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(mimetype="image/jpeg")
        red.save(response, "JPEG")
        return response
