from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *
from blog.models import Post
from gallery.models import *
from django.http import Http404
from fortnox.fortnox import get_headers, get_articles, get_article


import json
import requests
import httplib


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
    products = Variation.objects.filter(active=True, order__lte=100).order_by('-article__quality', '-order')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    return render_to_response('variation/index.html',
                             {'products': products,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

SIZES = ('XSmall', 'Small', 'Medium', 'Large', 'XLarge','XXLarge', )


def reaindex(request):

    products = ReaArticle.objects.filter(status='A').order_by('article__name')

    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True) 
    atypes = Type.objects.filter(order__lte=5, active=True)

    rea = "true"
    sizes = SIZES

    return render_to_response('variation/reaindex.html',
                             {'products': products,
                              'qualities': qualities,
                              'types': types,
                              'atypes': atypes,
                              'rea': rea, 
                              'sizes': sizes, 
                              },
                             context_instance=RequestContext(request))

def rea_by_size(request, key):
    products = ReaArticle.objects.filter(size__name = key, status='A').order_by('article__name')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    atypes = Type.objects.filter(order__lte=5, active=True)
    rea = "true"
    sizes = SIZES
    return render_to_response('variation/reaindex.html',
             {'products': products,
              'qualities': qualities,
              'types': types,
              'atypes': atypes,
              'rea': rea, 
              'sizes': sizes, },
        context_instance=RequestContext(request))


def rea_by_type(request, key):

    products = ReaArticle.objects.filter(article__type__order = key, status='A').order_by('article__name')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    atypes = Type.objects.filter(order__lte=5, active=True)
    rea = "true"
    sizes = SIZES
    return render_to_response('variation/reaindex.html',
             {'products': products,
              'qualities': qualities,
              'types': types,
              'atypes': atypes,
              'rea': rea, 
              'sizes': sizes, },
        context_instance=RequestContext(request))


def by_type(request, key):
    products = Variation.objects.filter(article__category__slug = key, order__lte=100, active=True).order_by('order', 'article__quality')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    return render_to_response('variation/index.html',
             {'products': products,
              'qualities': qualities,
              'types': types,},
        context_instance=RequestContext(request))


def by_quality(request, key):
    products = Variation.objects.filter(article__quality__slug__contains = key, order__lte=100, active=True).order_by('-order', 'article__quality')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
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

        if (product.article.quality.order == 13):
            sizes = Size.objects.filter(quality__pk = 1).order_by('-pk')
        else:
            sizes = Size.objects.filter(quality=product.article.quality).order_by('-pk')

        if (product.article.quality.order == 5 or product.article.quality.order == 14) :
            colorsandpattern = PatternAndColor.objects.filter(active=True, quality__slug ='silkestrika')
        else:
            colorsandpattern = PatternAndColor.objects.filter(active=True, quality=product.article.quality)
        

    except:
        raise Http404

    return render_to_response('variation/detail.html',
                   {
				   'product': product,
                   'images': images,
                   'colors': colors,
                   'patterns': patterns,
                   'sizes': sizes,
                   'qualities': qualities,
                   'types': types,
                   'color_id':color_id,
                   'pattern_id':pattern_id,
                   'products': products,
                   'colorsandpattern': colorsandpattern,
                   },
                   context_instance=RequestContext(request)
                   )

def readetail(request, pk):
    try:
        reaArticle = ReaArticle.objects.get(pk=pk)

    except:
        raise Http404

    return render_to_response('variation/readetail.html',
                   {'product': reaArticle,
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

def colorpatterntest(request):
    colorsandpattern = PatternAndColor.objects.filter(active=True, quality=1)

    return render_to_response('variation/colorandpatterntest.html',
                             {'colorsandpattern': colorsandpattern,
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

def reaarticle(request, pk):
    product = rea__Article.objects.get(pk=pk)
    product.stock = get_stockquantity(product)
    reatype = "rea"
    return render_to_response('rea/detail.html',
        {'product': product,
         'reatype': reatype,},
        context_instance=RequestContext(request))


def quality(request, name):
    pass

def category(request, name):
    pass

def allArticles(request): 
    headers = get_headers()
    articles = get_articles(headers)

    return render_to_response('variation/admin_view.html', {
        'articles': articles
    }, context_instance=RequestContext(request))


# to show all articels
def allArt(request):
    articles = Article.objects.filter(active = True).order_by('name')
    print articles

    headers = get_headers()
    check_art = []
    for art in articles: 
        try: 
            sku_num = int(art.sku_number)
            sku_num = str(sku_num)
        except: 
            sku_num = art.sku_number 
         
        res = get_article(headers, str(sku_num)) 
        res = json.loads(res)
        
        try:
            print res["ErrorInformation"]["Error"]
            check_art.append("error: " + str(art.sku_number) + " " + unicode(art.name))
        except:  
            print res['Article']['ArticleNumber']
            check_art.append("ok: " + unicode(res['Article']['ArticleNumber']) + " is the same " + str(art.sku_number))

    

    return render_to_response('variation/admin_view.html', {
        'articles': articles, 
        'check_art': check_art
    }, context_instance=RequestContext(request))

def allreaArt(request):
    reaarticles = ReaArticle.objects.all().order_by('status')
    
    return render_to_response('variation/admin_rea_art.html', {
        'articles': reaarticles, 

    }, context_instance=RequestContext(request))

