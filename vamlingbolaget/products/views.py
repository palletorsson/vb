from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *
from blog.models import Post

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
    variations = Variation.objects.all()
    print variations
    qualities = Quality.objects.all()
    types = Type.objects.all()
    images = Image.objects.all()
    products = zip(variations, images)
    print products
    return render_to_response('variation/index.html',
                             {'products': products,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

def by_type(request, key):
    same_types = Variation.objects.filter(article__type__slug = key)
    images = Image.objects.all()
    products = zip(same_types, images)
    qualities = Quality.objects.all()
    types = Type.objects.all()
    images = Image.objects.all()


    print same_types
    #same_color = Variation.objects.filter(combo__color__name = product.combo.color.name)
    #same_pattern = Variation.objects.filter(combo__pattern__name = product.combo.pattern.name)
    return render_to_response('variation/index.html',
             {'products': products,
              'qualities': qualities,
              'types': types,},
        context_instance=RequestContext(request))


def by_quality(request, key):
    same_quality = Variation.objects.filter(quality__slug = key)
    images = Image.objects.all()
    qualities = Quality.objects.all()
    types = Type.objects.all()
    products = zip(same_quality, images)
    return render_to_response('variation/index.html',
        {'products': products,
         'qualities': qualities,
         'types': types,},
        context_instance=RequestContext(request))


def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)
        name = product.name
        images = Variation.get_images(product, pk)
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

def show_galleries(request):
    galleries = Gallery.objects.all()
    num_gallery = galleries.count()
    return render_to_response('variation/gallery.html',
        {'galleries': galleries,
         'num_gallery' : num_gallery
        },
        context_instance=RequestContext(request)
    )

def show_gallery(request, key):
    gallery = Gallery.objects.get(pk=key)
    images = gallery.image_set.all()



    return render_to_response('variation/gallery.html',
        {'gallery': gallery,
         'images': images,
         'num_gallery' : 1

         },context_instance=RequestContext(request)
    )

def quality(request, name):
    pass

def category(request, name):
    pass
