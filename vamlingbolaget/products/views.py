from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *
from blog.models import Post
from gallery.models import *

def first_page(request):
    variations = Variation.objects.filter(active=True).order_by('article__quality')
    images = Image.objects.all()
    products = zip(variations, images)
    news = Post.objects.all()
    return render_to_response('variation/first_page.html',
							{'products': products,
							'news': news,
							},
							context_instance=RequestContext(request))


def index(request):
    products = Variation.objects.filter(active=True).order_by('order', 'article__quality')
    qualities = Quality.objects.filter(active=True)
    types = Type.objects.filter(active=True)
    return render_to_response('variation/index.html',
                             {'products': products,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

def by_type(request, key):
    products = Variation.objects.filter(article__type__slug = key, active=True).order_by('order', 'article__quality')
    qualities = Quality.objects.filter(active=True)
    types = Type.objects.filter(active=True)
    return render_to_response('variation/index.html',
             {'products': products,
              'qualities': qualities,
              'types': types,},
        context_instance=RequestContext(request))


def by_quality(request, key):
    products = Variation.objects.filter(article__quality__slug = key, active=True).order_by('order', 'article__quality')
    qualities = Quality.objects.filter(active=True)
    types = Type.objects.filter(active=True)
    return render_to_response('variation/index.html',
        {'products': products,
         'qualities': qualities,
         'types': types,},
        context_instance=RequestContext(request))


def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)

        products = Variation.objects.filter(article=product.article)

        images = Image.objects.filter(variation__pk=pk)
        color_id = product.color.order
        pattern_id = product.pattern.order
        qualities = Quality.objects.filter(active = True)
        types = Type.objects.filter(active = True)
        colors = Color.objects.filter(active=True, quality = product.article.quality)
        patterns = Pattern.objects.filter(active=True, quality = product.article.quality)
        sizes = Size.objects.filter(quality=product.article.quality)
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
                   'products': products,
                   },
                   context_instance=RequestContext(request)
                    )

def pattern_and_color(request):
    colors = Color.objects.filter(active=True, quality=1)
    patterns = Pattern.objects.filter(active=True, quality=1)

    return render_to_response('variation/combos.html',
                             {'colors': colors,
                              'patterns': patterns,
                              },
                             context_instance=RequestContext(request))


def bargain(request):
    products = Bargainbox.objects.filter(status='A')
    qualities = Quality.objects.filter(active=True)
    types = Type.objects.filter(active=True)
    return render_to_response('bargain/index.html',
        {'products': products,
        'qualities': qualities,
         'types': types,},
        context_instance=RequestContext(request))

def bargain_detail(request, pk):
    product = Bargainbox.objects.get(pk=pk)
    return render_to_response('bargain/detail.html',
        {'product': product,},
        context_instance=RequestContext(request))


def quality(request, name):
    pass

def category(request, name):
    pass

