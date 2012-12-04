from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Frontpage
from gallery.models import Gallery, Image
from blog.models import Post

def first_page(request):
    frontpage, created = Frontpage.objects.get_or_create(pk=1)
    gallery = Gallery.objects.filter(status__display_on_index_page = True) 
    images = Image.objects.filter(gallery=gallery)

    return render_to_response('frontpage/first_page.html',
        {'frontpage': frontpage,
         'gallery' : gallery,
         'images': images,
        },
        context_instance=RequestContext(request))
