from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import Project, Media, File, Kanban
import json
import contextlib
import os
import time


def index(request):
    projects = Project.objects.filter(status="A")
    projects_expired = Project.objects.filter(status="E")
    projects_public = Project.objects.filter(status="P")

    return render_to_response('projects/first_page.html',
							{'projects': projects, 
                             'projects_expired': projects_expired, 
                             'projects_public': projects_public, 
							},
							context_instance=RequestContext(request))

def detail(request, pk):
    temp_int = 1
    project = Project.objects.get(pk=pk)
    files = File.objects.filter(project=project)
    media = Media.objects.filter(project=project)
    kanban = Kanban.objects.filter(project=project)
       
    return render_to_response('projects/detail.html',
							{'project': project,
                             'files': files, 
                             'media': media,
                             'kanban': kanban,
							},
							context_instance=RequestContext(request))




