#-*-coding:iso-8859-1-*-
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response 
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Project, Media, File, Kanban
from products.models import *
from gallery.models import Gallery
import json
import contextlib
import os
import time
import re
import requests
import io
import urllib


@login_required
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

@login_required
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


@login_required
def transtest(request):
    hej = "testing translation"
    trans_root  = os.path.join(settings.ROOT_DIR, 'vamlingbolaget')
    input_root  = os.path.join(settings.ROOT_DIR, 'media')
    file_path = str(trans_root) + '/locale/django.po'    
    write_file = str(input_root) + '/w.text'
    word_list = []
    p = open(write_file, 'w+')
    limit = 0
    with open(file_path, 'r') as f:
        for line in f:
            if limit < 30:
                what = re.findall('^([\w\-]+)', line)
                if len(what) > 0:
                    if what[0] == 'msgstr': 
                        word = re.findall('\"(.*?)\"', line)
                        if word != None:     
                            word = word[0]
                            word = googleTranslate(word, 'fi')
                            line = re.sub(r'\"(.+?)\"','"'+word+'"', line)
                p.write(line)
            limit = limit + 1 

    return render_to_response('projects/tran.html',
                        {'hej': hej},
                          context_instance=RequestContext(request))


@login_required
def testtrans2(request, string, lang): 
    #hej = translatestring(request, string, lang)
    hej = full_tranlation(request, string, lang)
    print "maju"
    return render_to_response('projects/tran.html',
                    {'hej': hej},
                      context_instance=RequestContext(request))


@login_required
def transString(request, string, lang): 
    hej = translatestring(request, string, lang)
    return render_to_response('projects/tran.html',
                    {'hej': hej},
                      context_instance=RequestContext(request))

@login_required
def translatestring(request, string, lang): 
    url = 'https://www.googleapis.com/language/translate/v2?key=key&q='+string+'&source=sv&target='+lang
    resp = requests.get(url)
    return resp.content


@login_required
def full_tranlation(request, lang, model):
    tranlate_on = get_tranlatestatus()
    hej = 'no trans'
    count = 0
    
    if model == 'art':
        the_model = Article.objects.all()

    elif model == 'color':
        the_model = Color.objects.all()

    elif model == 'pattern':
        the_model = Pattern.objects.all()

    elif model == 'quality':
        the_model = Quality.objects.all()

    elif model == 'type':
        the_model = Type.objects.all()

    elif model == 'category':
        the_model = Category.objects.all()

    elif model == 'gallery':
        the_model = Gallery.objects.all()
  
    else: 
        hej = "now such model"
        return render_to_response('projects/tran.html',
                {'hej': hej},
                  context_instance=RequestContext(request))

    if tranlate_on == True: 
        for art in the_model:
            count = count + 1

            if count < 5:
                print "--" 
                name = art.name.encode('utf-8') 
                string = urllib.urlencode({'q': name})

                if lang == 'fi':
                    try: 
                        art.name_fi = googleTranslate(string, lang)
                        art.save()
                    except: 
                        pass
                elif lang == 'dk':
                    try: 
                        art.name_dk = googleTranslate(string, lang)
                        art.save()
                    except: 
                        pass
                elif lang == 'de':
                    try: 
                        art.name_de= googleTranslate(string, lang)
                        art.save()
                    except: 
                        pass
                elif  lang == 'all': 
                    try: 
                        art.name_fi = googleTranslate(string, lang)
                        art.name_dk = googleTranslate(string, lang)
                        art.name_de = googleTranslate(string, lang)
                        art.save()
                    except: 
                        pass                    
                else: 
                    hej = "now such language"
                    return render_to_response('projects/tran.html',
                            {'hej': hej},
                              context_instance=RequestContext(request))

                time.sleep(1)

        hej = "translate is on, art, color, pattern, quality, type, category, gallery"

    return render_to_response('projects/tran.html',
                    {'hej': hej},
                      context_instance=RequestContext(request))

          

def googleTranslate(string, lang): 

    api_key = "key"
    url = 'https://www.googleapis.com/language/translate/v2?key='+api_key+'&'+string+'&source=sv&target='+lang
    resp = requests.get(url)
    #print url
    the_content = json.loads(resp.content)
    print the_content
    try: 
        the_return = the_content['data']['translations'][0]['translatedText'].title()
    except: 
        the_return = "error"
    return the_return


def get_tranlatestatus():
    translate_on = True
    return translate_on

def printwords():
    input_file = str(input_root) + '/test3.csv'

    with open(input_file, 'r') as i:  
        for line in i:
            word_list.append(line)

    print word_list
