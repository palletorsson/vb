from django.http import HttpResponse
from django.shortcuts import render_to_response 
from django.template import RequestContext
from products.models import *
from blog.models import Post
from gallery.models import *
from django.http import Http404
from fortnox.fortnox import get_headers, get_articles, get_article, create_article, update_article
#from fortnox.local_fortnox import get_vb_headers
import json
from django.core import serializers
from collections import Counter
import csv
import os
from django.conf import settings


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

SIZES = ('XS', 'S', 'M', 'L', 'XL','XXL', )

def fullindex(request):
    full_variation = FullVariation.objects.filter(active=True).order_by('-order')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
  
    return render_to_response('variation/fullindex.html',
                             {'products': full_variation,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

def fullexport(request, what):
    full_variation = FullVariation.objects.filter(active=True).order_by('-order')

    for var in full_variation:
        print var.variation.article.sku_number, "|", var.variation.color, "|", var.variation.pattern, "|", var.size, "|", var.stock, "|"
        print str(var.variation.article.sku_number) + "_" + str(var.variation.color.order) + "_" + str(var.variation.pattern.order) + "_" + str(var.size)  

    return render_to_response('variation/fullindex.html',
                             {'products': full_variation,

                              },
                             context_instance=RequestContext(request))



def reaindex(request):

    products = ReaArticle.objects.filter(status='A').order_by('article__name')

    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True) 
    atypes = Type.objects.filter(order__lte=5, active=True)

    rea = "false"
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
def articleindex(request):

    articles = Article.objects.filter(active='A').order_by('name')

    return render_to_response('variation/articleindex.html',
                             {'articles': articles,

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

def product_api(request, key):
   
    product = Variation.objects.get(pk=key)
    print product


    resp_d = {'product': product.article.name}
    return HttpResponse(json.dumps(resp_d), content_type="application/json")



def detail(request, pk):
    try:
        product = Variation.objects.get(pk=pk)

        products = Variation.objects.filter(article=product.article).order_by('color')

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

    try:        
        images = Image.objects.filter(variation__pk=pk)
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

def fulldetail(request, pk):
    try:
        full_variation = FullVariation.objects.get(pk=pk)
        images = Image.objects.filter(variation__pk=full_variation.variation.pk)
        sizes = SIZES
    except:
        raise Http404

    full_variations_article = FullVariation.objects.filter(variation__article=full_variation.variation.article)    
    full_variations = FullVariation.objects.filter(variation=full_variation.variation)   

    init_sizes = ['XS','S','M','L', 'XL', 'XXL']

    size_list = []                           

    colorpattern_list = []


    for full_var in full_variations_article: 

        color_pattern_str = str(full_var.variation.color.order)+"f_"+str(full_var.variation.pattern.order)+"m"
        colorpattern_list.append(color_pattern_str)
    

    for full_var in full_variations: 
        size_list.append(full_var.size)

    variation_sizes = Counter(size_list)

    colorpattern_list = Counter(colorpattern_list)

    variation_sizes = list(variation_sizes)
    colorpattern_list = list(colorpattern_list)
    path_dir = settings.ROOT_DIR
    filename = str(full_variation.variation.article.sku_number) + "_" + str(full_variation.variation.color.order) + "_" + str(full_variation.variation.pattern.order) 

    images = [] 

    for x in range(0, 3):
        image = path_dir + "/media/variations/"+ filename +"_" + str(x+1) + ".jpg"        
        file_exist = os.path.isfile(image) 
        file = "/media/variations/"+ filename +"_" + str(x+1) + ".jpg"        
        if file_exist: 
          images.append(file)
  
    return render_to_response('variation/fulldetail.html',
                   {'product': full_variation,
                   'images': images,
                   'sizes': variation_sizes,
                   'colorsandpatterns': colorpattern_list,
                   'init_sizes': init_sizes, 
                   'full_variations': full_variations
                   },
                   context_instance=RequestContext(request)
                    )


def artdetail(request, pk):
    try:
        article_ = Article.objects.get(pk=pk)
    except:
        raise Http404

    products = Variation.objects.filter(article=article)
    return render_to_response('variation/artdetail.html',
                   {'article': article_,
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

def checkArticles(request): 
    headers = get_headers()  
    articles = get_articles(headers)

# to show all articels
def allArt(request):
    articles = Article.objects.filter(active = True).order_by('name')

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


def articleList(request):
    articles = Article.objects.filter(active = True).order_by('name')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    return render_to_response('articles/index.html',
                             {'articles': articles,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

def articlesCsv(request): 
    articles = Article.objects.filter(active = True).order_by('name')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = []

    for art in articles:
        temp = (art.name.encode('iso-8859-1'), art.sku_number)
        csv_data.append(temp)



    t = loader.get_template('articles/csv_temp.txt')
    c = Context({
        'data': csv_data,
    })
    response.write(t.render(c))
    return response



def articlesTranferToFortnox(request): 
    articles = Article.objects.filter(active = True).order_by('name')
    headers = get_headers()
    
    for art in articles: 
        try: 
            sku_num = int(art.sku_number)
            sku_num = str(sku_num)
        except: 
            sku_num = str(1) 

        res = get_article(headers, int(sku_num)) 
        data = json.dumps({
            "Article": {
                "Description": art.name,
                "ArticleNumber": int(sku_num), 
                "WebshopArticle": True, 
            }
        })
        
        if len(res) > 100: 
            exist = True
            updated = update_article(int(sku_num), data, headers)
            print updated 
        else: 
            exist = False
            created = create_article(int(sku_num), data, headers)
            print created   

    return HttpResponse(status=200)    
         
def articleUpdateStock(request, sku_num, stock): 
    sku_number = sku_num
    headers = get_headers()
    article = Article.objects.get(sku_number = sku_number)
    
    
    res = get_article(headers, sku_number) 
    data = json.dumps({
        "Article": {
            "Description": article.name,
            "ArticleNumber": 1401, 
            "QuantityInStock": stock, 
        }
    })
        
    if len(res) > 100: 
        exist = True
        updated = update_article(sku_number, data, headers)
        print updated 

    return HttpResponse(status=200)    


# article_sku, color, pattern, 1223_L02_MAH_01 1325_001_001_XL

