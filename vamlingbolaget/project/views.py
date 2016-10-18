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
from django.contrib.flatpages.models import FlatPage
import json
import contextlib
import os
import time
import re
import requests
import io
import urllib
from bs4 import BeautifulSoup

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
    trans_root  = os.path.join(settings.ROOT_DIR, 'vamlingbolaget')
    input_root  = os.path.join(settings.ROOT_DIR, 'media')
    file_path = str(trans_root) + '/locale/django.po'    
    write_file = str(input_root) + '/w.text'
    word_list = []
    p = open(write_file, 'w+')
    limit = 0
    with open(file_path, 'r') as f:
        for line in f:
            if limit < 1000:
                what = re.findall('^([\w\-]+)', line)
                if len(what) > 0:
                    if what[0] == 'msgstr': 
                        word = re.findall('\"(.*?)\"', line)
                        if word != None:     
                            word = word[0]
                            name = word.encode('utf-8') 
                            string = urllib.urlencode({'q': name})                            
                            word = googleTranslate(string, 'de')
                            line = re.sub(r'\"(.+?)\"','"'+word+'"', line)
                            line = line.encode('iso-8859-1')  
                p.write(line)
            limit = limit + 1 

    return render_to_response('projects/tran.html',
                        {'hej': hej},
                          context_instance=RequestContext(request))


@login_required
def transEmailMess(request):
    trans_root  = os.path.join(settings.ROOT_DIR, 'checkout')
    input_root  = os.path.join(settings.ROOT_DIR, 'media')
    file_path = str(trans_root) + '/messages.txt'    
    write_file = str(input_root) + '/h.text'
    word_list = []
    p = open(write_file, 'w+')
    limit = 0
    hej = "tranlating email messages"
    with open(file_path, 'r') as f:
        for line in f:
            if limit < 200:
                what = re.findall("\'(.*?)\'", line)
                print "-", what, len(what)
                if len(what) != 0:
                    if what != None or what != "#":  
                        word = what   
                        word = word[0]
                        name = word.encode('utf-8') 
                        string = urllib.urlencode({'q': name})                            
                        word = googleTranslate(string, 'fi')
                        print word
                        line = re.sub(r"\'(.*?)\'",'"'+word+'"', line)
                        line = line.encode('iso-8859-1')  
            p.write(line)
        limit = limit + 1 

    return render_to_response('projects/tran.html',
                        {'hej': hej},
                          context_instance=RequestContext(request))

@login_required
def testtrans2(request, string, lang): 
    #hej = translatestring(request, string, lang)
    hej = full_tranlation(request, string, lang)
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
            name = art.name.encode('utf-8') 
            string = urllib.urlencode({'q': name})

            if lang == 'fi':
                try: 
                    art.name_fi = googleTranslate(string, lang)
                    art.save()
                except: 
                    pass
            elif lang == 'da':
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

        hej = "translate is on, art, color, pattern, quality, type, category, gallery"

    return render_to_response('projects/tran.html',
                    {'hej': hej},
                      context_instance=RequestContext(request))

@login_required
def csvTransExport(request, model, what='title', lang='en'):
    tranlate_on = 1
    log = "no action"
    print model

    # mode to each model 
    if model == 'art':
        the_model = Article.objects.all()
        
    elif model == 'color':
        the_model = Color.objects.all()
        print the_model

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
        return render_to_response('projects/tran.html',
                {'hej': log},
                  context_instance=RequestContext(request))

    with open('modul_'+str(model)+'_'+str(what)+'_'+str(lang)+'.csv', 'w') as csvfile:
        if lang == 'fi':
            fieldnames = ['sv', 'fi', 'en',] 
        elif lang == 'de':
            fieldnames = ['sv', 'de', 'en',] 
        elif lang == 'dk':
            fieldnames = ['sv', 'dk', 'en',] 
        else:    
            writer.writerow({'sv': description_se, 'en': description_en,'fi': description_fi, 'de': description_de, 'dk': description_dk}) 
     
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if what == 'description': 

            if tranlate_on == True: 
                for art in the_model:
                    print art
                    description_se = art.description.encode('utf-8')
                    try: 
                        description_en = art.description_en.encode('utf-8') 
                    except: 
                        description_en = ''  
                    try:  
                        description_fi = art.description_fi.encode('utf-8') 
                    except: 
                        description_fi = '' 
                    # note that da here is demark      
                    try: 
                        description_dk = art.description_da.encode('utf-8')
                    except: 
                        description_dk = ''
                    try: 
                        description_de = art.description_de.encode('utf-8')          
                    except: 
                        description_de = ''
                    if lang == 'fi':
                        writer.writerow({'sv': description_se, 'fi': description_fi, 'en': description_en}) 
                    elif lang == 'de':
                        writer.writerow({'sv': description_se, 'de': description_de, 'en': description_en}) 
                    elif lang == 'dk':
                        writer.writerow({'sv': description_se, 'dk': description_dk, 'en': description_en}) 
                    else:    
                        writer.writerow({'sv': description_se, 'en': description_en,'fi': description_fi, 'de': description_de, 'dk': description_dk}) 
        else: 
            if tranlate_on == True: 
                for art in the_model:
                    title_se = art.name.encode('utf-8')
                    title_en = art.name_en.encode('utf-8') 
                    try:  
                        title_fi = art.name_fi.encode('utf-8') 
                    except: 
                        title_fi = ''    
                    try: 
                        title_dk = art.name_da.encode('utf-8')
                    except: 
                        title_dk = ''
                    try: 
                        title_de = art.name_de.encode('utf-8')          
                    except: 
                        title_de = ''

                    if lang == 'fi':
                        writer.writerow({'sv': title_se, 'fi': title_fi, 'en': title_en}) 
                    elif lang == 'de':
                        writer.writerow({'sv': title_se, 'de': title_de, 'en': title_en}) 
                    elif lang == 'dk':
                        writer.writerow({'sv': title_se, 'de': title_dk, 'en': title_en}) 
                    else:    
                        writer.writerow({'sv': title_se, 'en': title_en,'fi': title_fi, 'de': title_de, 'dk': title_dk}) 
       
        log = "exporting csv"

    return render_to_response('projects/tran.html',
                    {'hej': log},
                      context_instance=RequestContext(request))


@login_required
def csvTransImport(request, model, what='title', lang='en'):
    tranlate_on = 1
    log = "no action"

    if tranlate_on == True: 
        input_file = './modul_'+str(model)+'_'+str(what)+'_'+str(lang)+'.csv'
        print input_file
        count = 0  
        with open(input_file, 'r') as i:
            print i
            for line in i:
                if count > 0: 
                    print "line: ",  line

                    sepatated_values = line.split(",")
                    print sepatated_values
                
                    if what == 'description': 

                        try: 
                            description_se = sepatated_values[0]
                            #print title_se
                            description_en = sepatated_values[1]
                            #print title_en
                            description_fi = sepatated_values[2]
                            description_dk = sepatated_values[3]
                            description_de = sepatated_values[4]
                            if model == 'art':
                                art = Article.objects.get(description=description_se)    
                            elif model == 'quality':
                                art = Quality.objects.get(description=description_se)
                            elif model == 'type':
                                art = Type.objects.get(description=descriptione_se)
                            elif model == 'category':
                                art = Category.objects.get(description=description_se)
                            else: 
                                art = Article.objects.get(description=description_se)
                            print art 
                            art.name_en = title_en 
                            art.name_fi = title_fi 

                            try: 
                                art.name_da = title_dk
                            except: 
                                art.name_da = ''
                          
                            art.name_de = title_de
                            art.save()
                        except: 
                            pass
                    else:
                        
                        try: 
                            title_se = sepatated_values[0]
                            print title_se
                            if model == 'art':
                                art = Article.objects.get(name=title_se)    
                            elif model == 'color':
                                art = Color.objects.get(name=title_se)
                            elif model == 'pattern':
                                art = Pattern.objects.get(name=title_se)
                            elif model == 'quality':
                                art = Quality.objects.get(name=title_se)
                            elif model == 'type':
                                art = Type.objects.get(name=title_se)
                            elif model == 'category':
                                art = Category.objects.get(name=title_se)
                            else: 
                                art = Article.objects.get(name=title_se)
                            
                            if lang == 'fi':
                                art.name_fi = sepatated_values[1]
                                print  art.name_fi
                            elif lang == 'dk':
                                try: 
                                    art.name_da = sepatated_values[1] 
                                except: 
                                    pass     
                            elif lang == 'de':
                                art.name_de = sepatated_values[1]
                            else:    
                                art.name_en = title_en 
                                art.name_fi = title_fi 
                                try: 
                                    art.name_da = title_dk
                                except: 
                                    art.name_da = ''  
                                art.name_de = title_de
                            art.save()
                        except: 
                            pass            
                count = count + 1

    log = "importin csv"

    return render_to_response('projects/tran.html',
                    {'hej': log},
                      context_instance=RequestContext(request))



def translateflatpages(request, lang, pk):
    tranlate_on = get_tranlatestatus()
    hej = 'no trans'
    if tranlate_on == True: 
        #html = open("a.html",'r').read()
        hej = 'trans: ', lang
        the_page = FlatPage.objects.get(pk=pk)
        # translate title
        title = the_page.title_en
        string_ = urllib.urlencode({'q': title})                            
        new_title = googleTranslate(string_, lang) 
        
        if lang == 'fi':
            the_page.title_fi = new_title
        elif lang == 'da':
            the_page.title_da = new_title
        elif lang == 'de':
            the_page.title_de = new_title
        else: 
            hej = "now such language"
        # translate content
        html = the_page.content_en
        soup = BeautifulSoup(html, 'html.parser')

        for item in soup.findAll( "span", { "class" : "trans_text" }):
            original_string = item.contents[0]      
            trans_string = item.contents[0].encode('utf-8')
            string_ = urllib.urlencode({'q': trans_string})                            
            new_string = googleTranslate(string_, lang)       
            original_string.replace_with(new_string)
        

        if lang == 'fi':
            the_page.content_fi = soup.prettify('utf-8')
        elif lang == 'da':
            the_page.content_dk = soup.prettify('utf-8')
        elif lang == 'de':
            the_page.content_de = soup.prettify('utf-8')
        else: 
            hej = "now such language"

        the_page.save()

    return render_to_response('projects/tran.html',
                    {'hej': hej},
                      context_instance=RequestContext(request))

def googleTranslate(string, lang): 

    api_key = "key"
    url = 'https://www.googleapis.com/language/translate/v2?key='+api_key+'&'+string+'&source=sv&target='+lang
    resp = requests.get(url)
    the_content = json.loads(resp.content)
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
