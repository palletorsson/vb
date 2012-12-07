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
    
   
    return render_to_response('gallery/gallery.html',
        {'gallery': gallery,
         'num_gallery' : 1,
         'images':images,
         'break1':break1,
         'break2':break2,
         'break3':break3,
         },context_instance=RequestContext(request)
    )