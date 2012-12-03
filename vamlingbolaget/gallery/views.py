from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *

def show_galleries(request):
    galleries = Gallery.objects.filter(status__display_on_gallery_page = True)
    statuses = GalleryStatus.objects.filter(display_on_gallery_page = True) 
    num_galleries = galleries.count()
    return render_to_response('gallery/gallery.html',
        {'galleries': galleries,
         'statuses': statuses,
         'num_gallery': num_galleries,
        },
        context_instance=RequestContext(request)
    )

def show_gallery(request, key):
    gallery = Gallery.objects.get(pk=key)
    images = gallery.image_set.all()

    return render_to_response('gallery/gallery.html',
        {'gallery': gallery,
         'num_gallery' : 1,
         'images':images,
         },context_instance=RequestContext(request)
    )