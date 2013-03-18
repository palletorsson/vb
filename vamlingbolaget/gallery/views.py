from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *

def show_galleries(request):
    galleries = Gallery.objects.filter(status__display_on_gallery_page = True)
    statuses = GalleryStatus.objects.filter(display_on_gallery_page = True).order_by('order')
    num_galleries = galleries.count()
    return render_to_response('gallery/gallery.html',
        {'galleries': galleries,
         'statuses': statuses,
         'num_gallery': num_galleries,
        },
        context_instance=RequestContext(request)
    )

def show_gallery(request, key):
    if key == 'new':
        gallery = Gallery.objects.get(status__display_on_collection_page=True)
        template='gallery/collection.html'
    else:
        gallery = Gallery.objects.get(pk=key)
        template='gallery/gallery.html'

    images = gallery.image_set.all().order_by('order')
    num = len(images) + 1 #all images plus the feature image
    col = int(num/4) #images per column
    remaining = num % 4

    break1 = col-1 #think away the feature image which is not in a loop
    break2 = break1+col
    break3 = break2+col

    if remaining == 1:
        break1 = break1+1            
        break2 = break1+col
        break3 = break2+col
    elif remaining == 2:
        break1 = break1+1            
        break2 = break2+2            
        break3 = break2+col
    elif remaining == 3:
        break1 = break1+1            
        break2 = break2+2            
        break3 = break3+3            
    
   
    return render_to_response(template,
        {'gallery': gallery,
         'num_gallery' : 1,
         'images':images,
         'break1':break1,
         'break2':break2,
         'break3':break3,
         },context_instance=RequestContext(request)
    )