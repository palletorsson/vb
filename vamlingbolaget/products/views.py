from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render_to_response 
from django.template import RequestContext

from models import Variation

def index(request):
    products = Variation.objects.all()
    return render_to_response('variation/index.html',
                             {'products': products},
                             context_instance=RequestContext(request))

def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)
    except:
        return HttpResponse(404)
    print product.thumbnail
    return render_to_response('variation/detail.html',
                              {'product': product},
                              context_instance=RequestContext(request)
                              )



    
    