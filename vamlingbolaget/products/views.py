from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render_to_response 
from django.template import RequestContext

from models import Variation, Image

def index(request):
    try:
        products = Variation.objects.all()

    except:
        return HttpResponse(404)
    
    images = Image.objects.all()
    print images
    return render_to_response('variation/index.html',
                             {'products': products,
                              'images': images },
                             context_instance=RequestContext(request))

def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)
        name = product.name
        images = Variation.get_images(product, pk)
    except:
        return HttpResponse(404)

    return render_to_response('variation/detail.html',
                              {'product': product,
                               'images': images },
                              
                              context_instance=RequestContext(request)
                              )



    
    