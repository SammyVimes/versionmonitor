from tkinter import Image
from django.http import HttpResponse
from django.shortcuts import render
from versionmonitor import config
from versionmonitor.model.project import Project, ProjectMember

__author__ = 'Semyon'


def index(request):
    all_projects = Project.objects.all()
    context = {'projects': all_projects}
    return render(request, 'project/list.html', context)


def test(request):
    return render(request, 'project/test.html')


def upload_new_version_file(request, project_id):
    return render(request, 'project/test.html')


def project_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    versions = project.application.versions.all()
    last_version = -1
    v_count = versions.count()
    if v_count > 0:
        last_version = versions[v_count - 1].version_integer
    versions = reversed(list(versions))

    members = ProjectMember.objects.filter(project=project)

    context = {'project': project, 'versions': versions, 'last_version': last_version, 'members': members}
    return render(request, 'project/details.html', context)


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
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(mimetype="image/jpeg")
        red.save(response, "JPEG")
        return response

