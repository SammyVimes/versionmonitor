import os
from tkinter import Image
from django.http import HttpResponse
from django.shortcuts import render, redirect
from versionmonitor import config
from versionmonitor.model.project import Project, ProjectMember

__author__ = 'Semyon'


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
    user = request.user
    if not user or not user.is_authenticated():
        return redirect('/versionmonitor/login/')
    all_projects = __get_user_projects(user)
    context = {'projects': all_projects}
    return render(request, 'project/list.html', context)


def test(request):
    return render(request, 'project/test.html')


def upload_new_version_file(request, project_id):
    return render(request, 'project/test.html')


def project_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    user = request.user
    if not user or not user.is_authenticated():
        return redirect('/versionmonitor/login/')
    if not __check_user_access(user, project):
        return render(request, 'project/access_denied.html')
    versions = project.application.versions.all()
    last_version = -1
    v_count = versions.count()
    if v_count > 0:
        last_version = versions[v_count - 1].version_integer
    versions = reversed(list(versions))

    members = ProjectMember.objects.filter(project=project)

    context = {'project': project, 'versions': versions, 'last_version': last_version, 'members': members}
    return render(request, 'project/details.html', context)


def get_apk(request, project_id, version_integer):
    if int(version_integer) < 0:
        return None
    project = Project.objects.get(pk=project_id)
    user = request.user
    if not user or not user.is_authenticated():
        return redirect('/versionmonitor/login/')
    if not __check_user_access(user, project):
        return render(request, 'project/access_denied.html')
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
