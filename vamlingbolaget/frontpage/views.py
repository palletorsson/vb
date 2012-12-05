from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Frontpage
from gallery.models import Gallery, Image
from blog.models import New

def first_page(request):
    frontpage, created = Frontpage.objects.get_or_create(pk=1)
    gallery = Gallery.objects.filter(status__display_on_index_page = True) 
    images = Image.objects.filter(gallery=gallery)
    news = New.objects.filter(active=True).order_by('-publish_at')[:1]

    return render_to_response('frontpage/first_page.html',
        {'frontpage': frontpage,
         'gallery' : gallery,
         'images': images,
         'news': news,
        },
        context_instance=RequestContext(request))
