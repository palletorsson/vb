from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import Project, Media, File, Kanban
import json
import contextlib
import os
import time
import re
import requests
import io

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


def transtest(request):
    hej = "hej"
    trans_root  = os.path.join(settings.ROOT_DIR, 'vamlingbolaget')
    input_root  = os.path.join(settings.ROOT_DIR, 'media')
    file_path = str(trans_root) + '/locale/django.po'
    input_file = str(input_root) + '/test3.csv'
    write_file = str(input_root) + '/w.text'

    word_list = []

    with open(input_file, 'r') as i:  
        for line in i:
            word_list.append(line)

    print word_list
    a = -1

    p = open(write_file, 'w+')

    with open(file_path, 'r') as f:
 
        for line in f:

           
            what = re.findall('^([\w\-]+)', line)

            if len(what) > 0:

                if what[0] == 'msgstr': 
                    word = word_list[a].strip()  
                    line = re.sub(r'\"(.+?)\"','"'+word+'"', line)
                    print line 
                    a = a + 1
            p.write(line)



    return render_to_response('projects/tran.html',
                        {'hej': hej},
                          context_instance=RequestContext(request))


def testtrans2(request, string, lang): 
    hej = translatestring(request, string, lang)

    return render_to_response('projects/tran.html',
                    {'hej': hej},
                      context_instance=RequestContext(request))

def translatestring(request, string, lang): 
    url = 'https://www.googleapis.com/language/translate/v2?key=key&q='+string+'&source=sv&target='+lang
    resp = requests.get(url)
    return resp.content