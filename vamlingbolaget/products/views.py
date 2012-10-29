from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext

from models import Variation, ImageVariation, Combo, Color, Pattern, Size

def first_page(request):
	try:
		products = Variation.objects.all()
	except:
		return HttpResponse(404)
	
	return render_to_response('variation/first_page.html',
							  {'products': products,
							   },
							  context_instance=RequestContext(request))
	


def index(request):
    try:
        products = Variation.objects.all()
    except:
        return HttpResponse(404)

    images = ImageVariation.objects.all()
    products = zip(products, images)
    print products
    return render_to_response('variation/index.html',
                             {'products': products,  
                              },
                             context_instance=RequestContext(request))

def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)
        name = product.name
        images = Variation.get_images(product, pk)
        colors = Color.objects.all()
        patterns = Pattern.objects.all()
        sizes = Size.objects.all()
    except:
        return HttpResponse(404)

    return render_to_response('variation/detail.html',
                              {'product': product,
                               'images': images,
                   'colors': colors,
                   'patterns': patterns,
                   'sizes': sizes },
                              
                              context_instance=RequestContext(request)
                              )

def patternandcolor(request):
    try:
        combos = Combo.objects.all().order_by('color','-pattern' )
    except:
        return HttpResponse(404)

    return render_to_response('variation/combos.html',
                             {'combos': combos,  
                              },
                             context_instance=RequestContext(request))


    
    