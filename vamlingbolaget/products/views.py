from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *
from blog.models import Post
from gallery.models import *

def first_page(request):
    variations = Variation.objects.all()
    images = Image.objects.all()
    print images.image
    products = zip(variations, images)
    news = Post.objects.all()
    print news
    return render_to_response('variation/first_page.html',
							{'products': products,
							'news': news,
							},
							context_instance=RequestContext(request))




def index(request):
    products = Variation.objects.all()
    qualities = Quality.objects.all()
    types = Type.objects.all()
    return render_to_response('variation/index.html',
                             {'products': products,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

def by_type(request, key):
    products = Variation.objects.filter(article__type__slug = key)
    qualities = Quality.objects.all()
    types = Type.objects.all()
    return render_to_response('variation/index.html',
             {'products': products,
              'qualities': qualities,
              'types': types,},
        context_instance=RequestContext(request))


def by_quality(request, key):
    products = Variation.objects.filter(article__quality__slug = key)
    qualities = Quality.objects.all()
    types = Type.objects.all()
    return render_to_response('variation/index.html',
        {'products': products,
         'qualities': qualities,
         'types': types,},
        context_instance=RequestContext(request))


def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)
        images = Image.objects.filter(variation__pk=pk)
        color_id = product.color.order
        pattern_id = product.pattern.order
        colors = Color.objects.all()
        patterns = Pattern.objects.all()
        sizes = Size.objects.all()
        qualities = Quality.objects.all()
        types = Type.objects.all()
    except:
        return HttpResponse(404)

    return render_to_response('variation/detail.html',
                              {'product': product,
                               'images': images,
                   'colors': colors,
                   'patterns': patterns,
                   'sizes': sizes,
                   'qualities': qualities,
                   'types': types,
                   'color_id':color_id,
                   'pattern_id':pattern_id,
                   },
                   context_instance=RequestContext(request)
                    )

def pattern_and_color(request):
    colors = Color.objects.all()
    patterns = Pattern.objects.all()

    return render_to_response('variation/combos.html',
                             {'colors': colors,
                              'patterns': patterns,
                              },
                             context_instance=RequestContext(request))


def quality(request, name):
    pass

def category(request, name):
    pass
