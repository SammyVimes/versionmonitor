import os
import random
import string
from tkinter import Image
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import simplejson as simplejson
from versionmonitor import config
from versionmonitor.controller.push import create_user_token
from versionmonitor.model.project import Project, ProjectMember
from versionmonitor.model.usr import ApiUser
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


def login(request):
    username = request.POST["login"]
    password = request.POST["password"]
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        response = {
            'success': False,
            'reason': "USER_NOT_FOUND"
        }
        return HttpResponse(simplejson.dumps(response), content_type="application/json")
    correct = user.check_password(password)
    if correct:
        api_user = None
        try:
            api_user = ApiUser.objects.get(user=user)
        except ApiUser.DoesNotExist:
            pass
        if not api_user:
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            push_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            api_user = ApiUser(key=key, user=user, push_id=push_id)
            api_user.save()
        push_token, push_token_timestamp = create_user_token(api_user)
        response = {
            'key': api_user.key,
            'pushId': api_user.push_id,
            'pushToken': push_token,
            'pushTokenTimestamp': push_token_timestamp,
            'success': True
        }
        return HttpResponse(simplejson.dumps(response), content_type="application/json")
    else:
        response = {
            'success': False,
            'reason': "WRONG_PASSWORD"
        }
        return HttpResponse(simplejson.dumps(response), content_type="application/json")


login.csrf_exempt = True


def error(reason):
    return HttpResponse(simplejson.dumps({'error': reason}), content_type="application/json")


def __get_user(request):
    key = request.GET['key']
    api_user = None
    try:
        api_user = ApiUser.objects.get(key=key)
    except ApiUser.DoesNotExist:
        return None
    user = api_user.user
    return user


def __get_user_projects(user):
    project_members = None
    try:
        project_members = ProjectMember.objects.filter(user=user)
    except ProjectMember.DoesNotExist:
        return None
    all_projects = [member.project for member in project_members]
    return all_projects


def __check_user_access(user, project):
    try:
        return ProjectMember.objects.filter(user=user, project=project).count() > 0
    except ProjectMember.DoesNotExist:
        pass
    return False


def index(request):
    user = __get_user(request)
    if not user:
        return error('NOT_AUTHORIZED')
    all_projects = __get_user_projects(user)
    if not all_projects:
        return error('NOT_PARTICIPATING_IN_PROJECTS')
    projects = []
    response = {
        'projects': projects
    }
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
    return HttpResponse(simplejson.dumps(response), content_type="application/json")


def project_details(request, project_id):
    user = __get_user(request)
    if not user:
        return error('NOT_AUTHORIZED')
    project = Project.objects.get(pk=project_id)
    if not __check_user_access(user, project):
        return error('ACCESS_DENIED')
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
    user = __get_user(request)
    if not user:
        return error('NOT_AUTHORIZED')
    project = Project.objects.get(pk=project_id)
    if not __check_user_access(user, project):
        return error('ACCESS_DENIED')

    versions = project.application.versions
    version = versions.filter(version_integer=version_integer)[0]
    apk_uri = config.APPS_FOLDER + str(project.pk) + "/" + str(version.version_integer) + "/" + "app.apk"
    try:
        with open(apk_uri, "rb") as f:
            content_length = os.path.getsize(apk_uri)
            response = HttpResponse(f.read(), content_type="application/vnd.android.package-archive")
            response['Content-Length'] = content_length
            return response
    except IOError:
        return None


def version_icon(request, project_id, version_integer):
    if int(version_integer) < 0:
        return None
    project = Project.objects.get(pk=project_id)
    versions = project.application.versions
    version = versions.filter(version_integer=version_integer)[0]
    img_uri = config.APPS_FOLDER + str(project.pk) + "/" + str(version.version_integer) + "/" + "icon.png"
    try:
        with open(img_uri, "rb") as f:
            content_length = os.path.getsize(img_uri)
            response = HttpResponse(f.read(), content_type="image/jpeg")
            response['Content-Length'] = content_length
            return response
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(mimetype="image/jpeg")
        red.save(response, "JPEG")
        return response
