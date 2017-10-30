from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.template import RequestContext
from products.models import *
from blog.models import Post
from gallery.models import *
from django.http import Http404
from fortnox.fortnox import get_headers, get_articles, get_article, create_article, update_article, get_stockvalue, delete_article, getFortnoxSize, get_price, update_price
#from fortnox.local_fortnox import get_vb_headers
import json
from django.core import serializers
from collections import Counter
import csv
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
    full_variation = FullVariation.objects.filter(active=True, size=3840, variation__article__quality=1).order_by('variation__article', 'variation__article__category', 'order') 
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    return render_to_response('variation/fullindex.html',
                             {'products': full_variation,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))


def fullindexarticle(request):
    full_variation = Article.objects.filter(active='A').order_by('name')
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    return render_to_response('variation/fullindexarticle.html',
                             {'products': full_variation,
                              'qualities': qualities,
                              'types': types,
                              'rea': True
                              },
                             context_instance=RequestContext(request))


def fulllastindex(request):
    full_variation = FullVariation.objects.filter(size=3840, variation__article__quality=1).order_by('id')[:10] 
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    
    return render_to_response('variation/fullindex.html',
                             {'products': full_variation,
                              'qualities': qualities,
                              'types': types,
                              'rea': True
                              },
                             context_instance=RequestContext(request))


def fullindexQuality(request, quality):
    full_variation = FullVariation.objects.filter(active=True, size=3840, variation__article__quality__slug__contains = quality).order_by('order')
    qualities = Quality.objects.filter(active=True)

    if quality == 'plysch': 
        for item in full_variation: 
            item.oneimg = str(item.variation.article.sku_number) + "_" + str(item.variation.pattern.order) + "_" + str(item.variation.color.order) 


    types = Category.objects.filter(active=True)
  
    return render_to_response('variation/fullindex.html',
                             {'products': full_variation,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))


def fullindexlist(request):
    full_variation = FullVariation.objects.filter(active=True).order_by('-order')

    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
  
    return render_to_response('variation/fullindexlist.html',
                             {'products': full_variation,
                              'qualities': qualities,
                              'types': types,
                              },
                             context_instance=RequestContext(request))

def fullexport(request, what):
    full_variation = FullVariation.objects.filter(active=True, size=3840).order_by('order')

    for var in full_variation:
        print var.variation.article.sku_number, "|", var.variation.color, "|", var.variation.pattern, "|", var.size, "|", var.stock, "|"
        print str(var.variation.article.sku_number) + "_" + str(var.variation.color.order) + "_" + str(var.variation.pattern.order) + "_" + str(var.size)  

    return render_to_response('variation/fullindex.html',
                             {'products': full_variation,

                              },
                             context_instance=RequestContext(request))



def reaindex(request):

    products = ReaArticle.objects.filter(status='A').order_by('-article__name')

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

def reareact(request):
    rea = "true"
    sizes = SIZES
    atypes = Type.objects.filter(order__lte=5, active=True)
    return render_to_response('variation/reatest.html',
                             {
                              'rea': rea, 
                              'sizes': sizes, 
                              'atypes': atypes,
                              },
                             context_instance=RequestContext(request))


def jsonReaindex(request):
    products = ReaArticle.objects.filter(status='A').order_by('-article__name')
    allproducts = []
    for p in products:
        allproducts.append({
          "article": p.article.name,
          "sku": p.article.sku_number,
          "color": p.color.name,
          "pattern": p.pattern.name,
          "size": p.size.name, 
          "price": p.article.price,
          "reaprice": p.rea_price,
          "img": p.image.path, 
          "id": p.id
          })                  
    resp = json.dumps(allproducts)
    
    return HttpResponse(resp, content_type="application/json")

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

    products = ReaArticle.objects.filter(article__type__order = key, status='A').order_by('article__name').order_by('pattern').order_by('color')
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
    if key == 'kvinna':
        products = FullVariation.objects.filter(variation__article__category__slug = key, order__lte=100, size=3840, active=True).order_by('order')
        template = 'variation/fullindex.html'
    if key == 'man':
        products = FullVariation.objects.filter(variation__article__category__slug = key, size=3840, active=True).order_by('-order')
        template = 'variation/fullindex.html'
    else: 
        products = Variation.objects.filter(article__category__slug = key, order__lte=100, active=True).order_by('order', 'article__quality')
        template = 'variation/index.html'

    
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)

    return render_to_response(template,
             {'products': products,
              'qualities': qualities,
              'types': types,},
        context_instance=RequestContext(request))


def by_quality(request, key):
    template = 'variation/fullindex.html'
    if key == 'silkestrika':
        products = FullVariation.objects.filter(variation__article__quality__slug__contains = 'silkestrika', active=True, size=3840).order_by('order')
    elif key == 'manchester': 
        products = FullVariation.objects.filter(variation__article__quality__slug__contains = 'manchester', active=True, size=3840).order_by('order')
    elif key == 'plysch': 
        products = FullVariation.objects.filter(variation__article__quality__slug__contains = 'plysch', active=True, size=3840).order_by('order')
        template = 'variation/plyschindex.html'
    else: 
        products = Variation.objects.filter(article__quality__slug__contains = key, order__lte=100, active=True).order_by('-order', 'article__quality')
        template = 'variation/index.html'
     
    qualities = Quality.objects.filter(active=True)
    types = Category.objects.filter(active=True)
    return render_to_response(template,
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


def articleDetail(request, pk):
    try:
        product = Article.objects.get(pk=pk)
        products = FullVariation.objects.filter(variation__article=product, size='3840', active=True)

        for full_var in products: 
            color_pattern_str = str(full_var.variation.color.order)+"f_"+str(full_var.variation.pattern.order)+"m"
            full_var.cp = color_pattern_str
            num = int(full_var.pk)
            link = "/products/fullvariation/"+ str(num) + "/#" + str(full_var.variation) + " " + str(full_var)
            full_var.link = link
            filename = str(full_var.variation.article.sku_number) + "_" + str(full_var.variation.pattern.order) + "_" + str(full_var.variation.color.order) 
            file = "/media/variations/"+ filename +"_1.jpg"  
            full_var.image = file   
        
        qualities = Quality.objects.filter(active = True)
        types = Type.objects.filter(active = True)
        colors = Color.objects.filter(active=True, quality = product.quality)
        patterns = Pattern.objects.filter(active=True, quality = product.quality)

        if (product.quality.order == 13):
            sizes = Size.objects.filter(quality__pk = 1).order_by('-pk')
        else:
            sizes = Size.objects.filter(quality=product.quality).order_by('-pk')
        
        if (product.quality.order == 5 or product.quality.order == 14):
            colorsandpattern = PatternAndColor.objects.filter(active=True, quality__slug ='silkestrika')
        else:
            colorsandpattern = PatternAndColor.objects.filter(active=True, quality=product.quality)
        

     
    except:
        raise Http404 

    try:        
        images = Image.objects.filter(variation__pk=pk)
    except:
        raise Http404 

    copa_res = []
    for copa in colorsandpattern: 
        splited = copa.name.split("&")
        if len(splited) > 1: 
            print "-"
        else: 
            copa_res.append(copa)
            print "+"
    print copa_res

    return render_to_response('variation/articledetail.html',
                   {
                   'product': product,
                   'images': images,
                   'colors': colors,
                   'patterns': patterns,
                   'sizes': sizes,
                   'qualities': qualities,
                   'types': types,
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
    except:
        raise Http404

    colorsandpatterns = PatternAndColor.objects.filter(active=True, quality__slug ='silkestrika')

    full_variations_article = FullVariation.objects.filter(variation__article=full_variation.variation.article, size="42")  

    full_variations = FullVariation.objects.filter(variation=full_variation.variation)   

    init_sizes = ['XS','S','M','L', 'XL', 'XXL']

    size_list = []                           

    for full_var in full_variations_article: 
        color_pattern_str = str(full_var.variation.color.order)+"f_"+str(full_var.variation.pattern.order)+"m"
        full_var.cp = color_pattern_str
        num = int(full_var.pk)
        link = "/products/fullvariation/"+ str(num) + "/#" + str(full_var.variation) + " " + str(full_var)
        full_var.link = link
        filename = str(full_var.variation.article.sku_number) + "_" + str(full_var.variation.pattern.order) + "_" + str(full_var.variation.color.order) 
        file = "/media/variations/"+ filename +"_1.jpg"  
        full_var.image = file   


    #mapping name size to number
    for full_var in full_variations:

        if full_var.size == '34':         
            size_list.append('XS')
            full_var.lettersize = 'XS'
        elif full_var.size == '36': 
            size_list.append('S')   
            full_var.lettersize =  'S' 
        elif full_var.size == '3840': 
            size_list.append('M')  
            full_var.lettersize = 'M'
        elif full_var.size == '42': 
            size_list.append('L') 
            full_var.lettersize = 'L' 
        elif full_var.size == '44': 
            size_list.append('XL')
            full_var.lettersize = 'XL'  
        elif full_var.size == '46':
            size_list.append('XXL')
            full_var.lettersize =  'XXL'  
        else: 
            print "no such size"

    variation_sizes  = f7(full_variations)

    full_variations_article = Counter(full_variations_article) 
    full_variations_article = list(full_variations_article)

    path_dir = settings.ROOT_DIR
    filename = str(full_variation.variation.article.sku_number) + "_" + str(full_variation.variation.pattern.order) + "_" + str(full_variation.variation.color.order) 

    images = [] 

    for x in range(0, 3):
        file = "/media/variations/"+ filename +"_" + str(x+1) + ".jpg"        
        images.append(file)

    stock_value = full_variation.stock

    return render_to_response('variation/fulldetail.html',
                   {'product': full_variation,
                   'images': images,
                   'sizes': variation_sizes,
                   'init_sizes': init_sizes, 
                   'full_variations': full_variations, 
                   'stock_value': stock_value,
                   'full_variations_article': full_variations_article, 
                   'colorsandpatterns': colorsandpatterns
                   },
                   context_instance=RequestContext(request)
                    )

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x.size in seen or seen_add(x.size))]

def artdetail(request, pk):
    try:
        article_ = Article.objects.get(pk=pk)
    except:
        raise Http404

    products = Variation.objects.filter(article=article_)
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
    articles = get_articles(headers, 1)

    return render_to_response('variation/admin_view.html', {
        'articles': articles
    }, context_instance=RequestContext(request))

@login_required
def variationduplicates(request, remove): 
    variation = Variation.objects.all()
    uniq = []
    for var in variation:
        greg = str(var.article.sku_number) + "_" + str(var.pattern) + "_" + str(var.color)  
        if greg not in uniq: 
            uniq.append(greg)
            print "---------", greg
        else:
            print greg
            if remove == 1: 
                var.delete()
    print uniq        
    return HttpResponse(status=200)

# to show all articels
def allArt(request, what='', start_at=1, end_at=10):

    status = ''
    indx = int(start_at)

    articles = Article.objects.filter(active = True).order_by('name')
    full_variations = FullVariation.objects.filter(active=True) 

    headers = get_headers()
    check_art = []
    new_art_set = []

    for fullvar in full_variations: 
        data = {}
        art_num = str(fullvar.variation.article.sku_number) + "_" + str(fullvar.variation.pattern.order) + "_" + str(fullvar.variation.color.order) + "_" + str(fullvar.size) 
        
        data["Article"] = {}
        data["Article"]["Description"] = unicode(fullvar)
        data["Article"]["ArticleNumber"] = art_num
        data["Article"]["Price"] = str(fullvar.variation.article.price)

        new_art_set.append(data) 
    
    for art in articles:
        data = {}
        art_num = art.sku_number

        data["Article"] = {}
        data["Article"]["Description"] = unicode(art)
        data["Article"]["ArticleNumber"] = art_num
        data["Article"]["Price"] = str(art.price)
        new_art_set.append(data) 
    
    art_length = len(new_art_set)
    
    for art in new_art_set: 
        indx = indx + 1
        if indx > 1 and indx > int(start_at) and indx < int(end_at):
            sku_num = art['Article']['ArticleNumber']
            descript = art['Article']['Description']

            res = get_article(headers, str(sku_num)) 
            res = json.loads(res)

            if what == 'look':
                try:
                    check_art.append(str(indx) + " : " + str(sku_num) + " - " + unicode(res['Article']['Description']))
                except:  
                    check_art.append("error: " + str(sku_num))
            
            elif what == 'addifnotexist': 

                try:
                    check_art.append("Exist: " + str(sku_num) + " " + unicode(res['Article']['Description'])) 
                    status = 'found'
                except:  
                    status = 'notfound'

                if status == "notfound": 
                    check_art.append("Add ------------ Article: " + unicode(sku_num))
                    data = json.dumps({
                    "Article": {
                        "Description": unicode(descript),
                        "ArticleNumber": unicode(sku_num), 
                        "WebshopArticle": True, 
                      }
                    })
                    created = create_article(str(sku_num), data, headers)
                    check_art.append(created)


            elif what == 'setprice': 
                check_art.append("Add ------------ Price: " + unicode(sku_num))
                price_res = get_price(str(sku_num), headers)
                check_art.append(price_res)
                price = json.loads(price_res)
                
                try: 
                    if price['ErrorInformation']['code'] != '': 
                        status = 'pricenotset'
                except: 
                    status = 'priceexist'

                status = 'pricenotset'

                if status == "pricenotset":
                    data = json.dumps({
                          "Price": {
                            "ArticleNumber": unicode(sku_num),
                            "FromQuantity": 1,
                            "Price": int(art["Article"]["Price"]), 
                            "PriceList": "A"
                        }
                    })  
                    updated = update_price(data, headers)
            else:
                print "no of the above"

   
    return render_to_response('variation/admin_view_update.html', {
        'articles': articles, 
        'check_art': check_art,
        'art_length': art_length
    }, context_instance=RequestContext(request))


def allFullArt(request, quality):

    full_variations = FullVariation.objects.filter(active=True, variation__article__quality__slug__contains=quality)
    
    headers = get_headers()
    check_art = []

    products = agigateFortnoxProducts()
    
    for art in full_variations: 
        art_exist = False
        sku_num = str(art.variation.article.sku_number) + "_" + str(art.variation.pattern.order) + "_" + str(art.variation.color.order) + "_" +  str(art.size)     
        
        res = get_article(headers, sku_num) 
        res = json.loads(res)
        
        try:
            d = res['Article']['ArticleNumber']
            check_art.append("ok")
            art_exist = True 
        except:  
            check_art.append("error: " + str(art.variation.article.sku_number) + " **** " + unicode(art.variation.article))
            headers = get_headers()

        if art_exist == False:    
            article_name = unicode(art.variation.article.name) + " " + unicode(art.variation.pattern) + " " + unicode(art.variation.color) + " " + unicode(art.size)
                 
            data = json.dumps({
                "Article": {
                    "Description": article_name ,
                    "ArticleNumber": sku_num, 
                    "WebshopArticle": True, 
                }
            })
            created = create_article(sku_num, data, headers)

    return render_to_response('variation/admin_view.html', {
        'articles': full_variations, 
        'check_art': check_art
    }, context_instance=RequestContext(request))

def agigateFortnoxProducts(): 
    allart = []
    headers = get_headers()
    for page in range(0, 9):
        allart_part = get_articles(headers, str(page))  
        allart_part = json.loads(allart_part)
        try: 
            products = allart_part['Articles']

            for product in products: 

                allart.append(product['ArticleNumber'])
        except: 
            pass
    return allart 

def checkConsistDjangoFortnox(request): 
    
    # get all variation and articles from django 
    articles = Article.objects.filter(active=True)
    # get fortnox headers
    headers = get_headers()
    for art in articles: 
      article_check = get_article(headers, art.sku_number)
      print article_check

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

def fromCsvToFortnox(name, sku_number, stock_value): 

    headers = get_headers()
    data = json.dumps({
        "Article": {
            "Description": name,
            "ArticleNumber": sku_number, 
            "QuantityInStock": int(stock_value), 
        }
    })
    error_or_create = create_article(sku_number, data, headers)

    return error_or_create   
              
def fromCsvToFortnoxUpdate(name, sku_number, stock_value):
    headers = get_headers()
    data = json.dumps({
        "Article": {
            "Description": name,
            "ArticleNumber": sku_number, 
            "QuantityInStock": float(stock_value), 
        }
    })

    # If product exist the error message look like : {"ErrorInformation":{"error":1,"message":"Artikelnumret \"1510_7_6_46\" \u00e4r redan taget.","code":2000013}}
    # then only update the product
    try:
        update_art = update_article(sku_number, data, headers)
    except:
        update_art = "error -------------"
        pass

    return update_art 

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

# import or update fullvaration from csv                     
def fromCsvToDjango(article, pattern, color, size, stock):
    no_simpel_create = 0
    print "je", article, pattern, color, size, stock
    try: 
        variation, created_variation = Variation.objects.get_or_create(article=article, pattern=pattern, color=color)
    except: 
        no_simpel_create = 1
    # 
    if no_simpel_create == 1: 
        variation = Variation.objects.filter(article=article, pattern=pattern, color=color)[0]
        print "one var", variation


    fullvariation, created_fullvariation = FullVariation.objects.get_or_create(variation=variation, size=size, stock=stock)
    # if fullvariation exist only update the fullvaration with stockvalue
    if created_fullvariation == False: 
        fullvariation.stock = stock
        print "---_"
        fullvariation.save()
    return True

def fromCsvToDjangoDisable(article, pattern, color, size):
    no_simpel_create = 0

    try: 
        variation = Variation.objects.get(article=article, pattern=pattern, color=color)
    except: 
        no_simpel_create = 1

    if no_simpel_create == 1: 
        variation = Variation.objects.filter(article=article, pattern=pattern, color=color)[0]
        print "one var", variation


    fullvariation = FullVariation.objects.get(variation=variation, size=size)

    # if fullvariation exist only update the fullvaration with stockvalue
    try: 
        fullvariation.active = False
        fullvariation.save()
    except: 
        print "disable error"

    return True

#read csv and insert full varations or products ini django database and fortnox 

@login_required         
def readCsvOnlyCheck(request):
    path_dir = settings.ROOT_DIR
    input_file = './modeller.csv'
    count = 0 
    # open file and sepate values 
    articles = []
    images = []
    filefails = [] 
    check_art = "mjau"
    with open(input_file, 'r') as i:
        for line in i:
            sepatated_values = line.split(",")
            count = count + 1 
            img_count = 1
            # see if values exist 

            if sepatated_values[1] != '' and count > 1: 
                stock = sepatated_values[2]
                if stock == '':
                    stock = 0
 
                full_article_sku = sepatated_values[1]
                #pattern first
                #split and get values from 1223_10_12_36 - article_sku, pattern, color, size 
                splitart = full_article_sku.split("_")
                try: 
                    article = Article.objects.get(sku_number=splitart[0])
                except:
                    article = "no article"

                try: 
                    color = Color.objects.get(order=splitart[2])
                except: 
                    color = "no color"
                try:       
                    pattern = Pattern.objects.get(order=splitart[1])
                except: 
                    color = "no pattern"      

                size = splitart[3]

                img_name = splitart[0] + "_" + splitart[1] + "_" + splitart[2] + "_" + str(img_count) 
                image = path_dir + "/media/variations/"+ str(img_name) + ".jpg"   
                #print image     
                file_exist = os.path.isfile(image) 

                if file_exist: 
                    image = "ok: " + img_name
                else: 
                    image = "fail: " + img_name + " - " + str(article) + " - " + str(color) + " - " + str(pattern)
                    if size == '3840':

                        filefails.append(image)


                check = str(article) + " " + str(pattern) + " " + str(color) + " " + str(size) + "  " + str(full_article_sku) + " --  " + str(sepatated_values[0])
                articles.append(check)
                images.append(image)

                img_count = img_count + 1
                #print img_count 
                if img_count == 4:
                    img_count = 1

            else: 
                pass 

    return render_to_response('variation/csv_view.html', {
        'articles': articles, 
        'images': images, 
        'failed': filefails
    
    }, context_instance=RequestContext(request))

#read csv and insert full varations or products ini django database and fortnox          
#url(r'^readcsv/(?P<what>[a-zA-Z0-9_.-]+)/$', 'readCsv'),
@login_required
def readCsv(request, what, start_at, end_at):
    input_file = './modeller.csv'
    count = 0 
    articles = []
    images = []
    filefails = [] 
    # open file and sepate values 
    with open(input_file, 'r') as i:
        for line in i:
            sepatated_values = line.split(",")
            count = count + 1 
            # see if values exist 
            start_at = int(start_at)
            end_at = int(end_at)
            stock = sepatated_values[2]

            if sepatated_values[1] != '' and count > 1 and count > start_at and count < end_at: 
                print "read this line"
                stock = sepatated_values[2]
                if stock == '':
                    stock = 0

                full_article_sku = sepatated_values[1]
                #split and get values from 1223_10_12_36 - article_sku, color, pattern, size 
                splitart = full_article_sku.split("_")
                article_name_ = ''
                try: 
                    article = Article.objects.get(sku_number=splitart[0])
                    color = Color.objects.get(order=splitart[2])
                    pattern = Pattern.objects.get(order=splitart[1])
                    size = splitart[3]
                    article_name_ = unicode(article.name) + " " + unicode(pattern) + " " + unicode(color) + " " + unicode(size)
                    print article_name_
                    articles.append(article_name_)
                except:
                    print "art wrong ", count, sepatated_values[1]
                    articles.append("-------------")
                    

                if what == "fortnox": 
                    # insert or update product in fortnox       
                    try:
                        error_or_create = fromCsvToFortnox(article_name_, full_article_sku, stock)
                        filefails.append(error_or_create)
                        #print article_name
                        #print error_or_create
                    except:
                        pass
                        #print "fortnox wrong ", count, sepatated_values[1]

                elif what == "updatefortnox": 
                    print "update: ", article_name_ 
                    # insert or update product in fortnox       
                    try:
                        # get the stock value and update name 
                        try: 
                            variation = Variation.objects.filter(article=article, pattern=pattern, color=color)[0]
                            full_var = FullVariation.objects.get(variation=variation, size=size)
                            stock = full_var.stock
                        except:
                            pass
                        #print full_var, size, article_name_, full_article_sku, stock
                        #print error_or_create
                        try: 
                            sizename = getFortnoxSize(size)
                            article_n = article_name_ + str(" (" + sizename +")")
                        except:
                            article_n = article_name_
                                
                        error_or_create = fromCsvToFortnoxUpdate(article_n, full_article_sku, stock)
                        print error_or_create
                        filefails.append(error_or_create)
                    except:
                        pass
                        #print "fortnox wrong ", count, sepatated_values[1]

                elif what == "django": 
                    # insert or update full_variation
                    stock = 10
                    try:
                        fromCsvToDjango(article, pattern, color, size, stock)
                    except: 
                        print "django wrong ", count, sepatated_values[1]
                elif what == "djangodisable": 
                    # insert or update full_variation

                    stock = 10
                    try:
                        fromCsvToDjangoDisable(article, pattern, color, size)
                    except: 
                        print "django wrong ", count, sepatated_values[1]
                else: 
                    print "hej"            
            else: 
                pass
    return render_to_response('variation/csv_view.html', {
        'articles': articles, 
        'images': images, 
        'failed': filefails
    
    }, context_instance=RequestContext(request))

@login_required
def readCsvManchester(request, what, start_at, end_at):
    input_file = './manchester.csv'
    count = 0 
    articles = []
    images = []
    filefails = []
    # open file and sepate values 
    with open(input_file, 'r') as i:
        for line in i:
            sepatated_values = line.split(",")

            count = count + 1 
            # see if values exist 
            start_at = int(start_at)
            end_at = int(end_at)
            stock = sepatated_values[2]

            if sepatated_values[1] != '' and count > 1 and count > start_at and count < end_at: 
                stock = sepatated_values[4]
                if stock == '':
                    stock = 0

                full_article_sku = sepatated_values[1]
                #split and get values from 1223_10_12_36 - article_sku, color, pattern, size 
                splitart = full_article_sku.split("_")
                try: 
                    article = Article.objects.get(sku_number=splitart[0])
                    color = Color.objects.get(order=splitart[2])
                    pattern = Pattern.objects.get(order=splitart[1])
                    size = splitart[3]
                    article_name_ = unicode(article.name) + " " + unicode(pattern) + " " + unicode(color) + " " + unicode(size)
                    articles.append(article_name_)
                except:
                    print "art wrong ", count, sepatated_values[1]
                    article_name_ = ''
                    articles.append(article_name_)

                if what == "fortnox": 
                    # insert or update product in fortnox       
                    try:
                        try: 
                            sizename = getFortnoxSize(size)
                            article_n = article_name_ + str(" (" + sizename +")")
                            articles.append(article_name_)
                        except:
                            article_n = article_name_
                            articles.append(article_name_)

                        print "art --- ", article_n, full_article_sku   
                        error_or_create = fromCsvToFortnox(article_n, full_article_sku, stock)
                        #print error_or_create
                    except:
                        pass
                        #print "fortnox wrong ", count, sepatated_values[1]

                elif what == "updatefortnox": 
                  print "update: ", article_name_ 
                  # insert or update product in fortnox

                  try:
                      # get the stock value and update name 
                      try: 
                          variation = Variation.objects.filter(article=article, pattern=pattern, color=color)[0]
                          full_var = FullVariation.objects.get(variation=variation, size=size)
                          stock = full_var.stock
                      except:
                          pass
                      #print full_var, size, article_name_, full_article_sku, stock
                      #print error_or_create
                      try: 
                          sizename = getFortnoxSize(size)
                          article_n = article_name_ + str(" (" + sizename +")")
                          articles.append(article_n)
                      except:
                          article_n = article_name_
                          articles.append(article_n)
                              
                      error_or_create = fromCsvToFortnoxUpdate(article_n, full_article_sku, stock)
                      print error_or_create
                      filefails.append(error_or_create)
                  except:
                      pass
                      #print "fortnox wrong ", count, sepatated_values[1]

                elif what == "django": 
                    # insert or update full_variation
                    print splitart[0]
                    fromCsvToDjango(article, pattern, color, size, stock)

                else: 
                    print "hej"            
            else: 
                pass
    return render_to_response('variation/csv_view.html', {
        'articles': articles, 
        'images': images, 
        'failed': filefails
    
    }, context_instance=RequestContext(request))

@login_required
def removeCsv(request, start_at, end_at):
    input_file = './modeller.csv'
    count = 0 
    header = get_headers()
    # open file and sepate values 
    with open(input_file, 'r') as i:
        for line in i:
            sepatated_values = line.split(",")
            count = count + 1 
            # see if values exist 

            if sepatated_values[1] != '' and count > 1 and count > start_at and count < end_at: 
                print "read this line"
                stock = sepatated_values[2]
                if stock == '':
                    stock = 0

                full_article_sku = sepatated_values[1]
                del_art = delete_article(header, full_article_sku)
                print del_art

    return HttpResponse(status=200)

# 10, 6, 8, 
@login_required
def removeByColor(request, color, act):
    print "remove color: " + str(color)
    count = 0 
    fullart_bycolor = FullVariation.objects.filter(variation__article__quality=1, variation__color__order=int(color)) 
    print fullart_bycolor
    for art in fullart_bycolor: 
        print art.variation.color
        if int(act) == 1: 
            art.active = True
        else:
            art.active = False  
        art.save()

    return HttpResponse(status=200)


@login_required
def orderCsv(request):
    input_file = './order.csv'
    count = 0 
    sizes = [34, 36, 3840, 42, 44, 46]
    # open file and sepate values 
    with open(input_file, 'r') as i:

        for line in i:
            #print line 
            sepatated_values = line.split(",")
            count = count + 1 
            # see if values exist 
            if sepatated_values[0] != '': 
                art_and_partner = sepatated_values[0] 
                splitart = art_and_partner.split("_")

                try: 
                    article = Article.objects.get(sku_number=splitart[0])
                    pattern = Pattern.objects.get(order=splitart[1])
                    color = Color.objects.get(order=splitart[2])
                    variation = Variation.objects.get(article=article, pattern=pattern, color=color)
                    print variation 
                    order = 100 + count
                    print art_and_partner, splitart, order
                    for size in sizes: 
                         
                        try:
                            fullvar = FullVariation.objects.get(variation=variation, size=size)
                            fullvar.order = order
                            fullvar.save()
                        except:
                            print "no such size"
                        print fullvar
                except:
                    print "error"


    return HttpResponse(status=200)
@login_required
def setfullstockCsv(request):
    input_file = './modeller.csv'

    # open file and sepate values 
    with open(input_file, 'r') as i:

        for line in i:
            sepatated_values = line.split(",")
            print sepatated_values
            if sepatated_values[1] != '': 
                art_and_partner = sepatated_values[1] 
                splitart = art_and_partner.split("_")
                print splitart 
                try: 
                    print art_and_partner, splitart
                    article = Article.objects.get(sku_number=splitart[0])
                    pattern = Pattern.objects.get(order=splitart[1])
                    color = Color.objects.get(order=splitart[2])
                    variation = Variation.objects.get(article=article, pattern=pattern, color=color)
                    print variation 
                    print splitart[3]
                    fullvar = FullVariation.objects.get(variation=variation, size=splitart[3])
                    fullvar.stock = sepatated_values[2]
                    print sepatated_values[2]
                    fullvar.save()
                    print "it worked"
                except:
                    print "error"


    return HttpResponse(status=200)

@login_required
def downFromCsv(request):
    input_file = './downlist.csv'

    # open file and sepate values 
    with open(input_file, 'r') as i:
        for line in i:
            #print line 
            sepatated_values = line.split(",")
            # see if values exist 
            if sepatated_values[0] != '': 
                fullart = sepatated_values[0] 
                splitart = fullkey.split("_")
                article = Article.objects.get(sku_number=splitart[0])
                pattern = Pattern.objects.get(order=splitart[2])
                color = Color.objects.get(order=splitart[1])
                size = splitart[3]
                variation = Variation.objects.get(article=article, pattern=pattern, color=color)
                fullvar = FullVariation.objects.get(variation=variation, size=size)
                if (fullvar.stock > 0): 
                    fullvar.stock = fullvar.stock - 1 
                    fullvar.save()    
                print fullvar.stock
    return HttpResponse(status=200)

@login_required
def FullDown(request, fullkey):
    splitart = fullkey.split("_")
    article = Article.objects.get(sku_number=splitart[0])
    pattern = Pattern.objects.get(order=splitart[2])
    color = Color.objects.get(order=splitart[1])
    size = splitart[3]
    variation = Variation.objects.get(article=article, pattern=pattern, color=color)
    fullvar = FullVariation.objects.get(variation=variation, size=size)
    if (fullvar.stock > 0): 
        fullvar.stock = fullvar.stock - 1 
        fullvar.save()    
    print fullvar.stock

    return HttpResponse(status=200)


@login_required
def setDiscount(request, what=''):
    discount = None
    articles = Article.objects.all()
    if what == 'set': 
        discount = Discount.objects.get(reason='survive2016')
    elif what == 'reset': 
        discount = None
    elif what == 'setplysch20': 
        discount = Discount.objects.get(reason='plysch20') 
        articles = Article.objects.filter(quality__slug__contains = 'plysch')
    else: 
        discount == False

    if discount != False:     
        for art in articles:
          art.discount = discount 
          art.save()
    return HttpResponse(status=200)

@login_required
def setPriceFromlist(request):
    input_file = './newprices.csv'
    count = 0 
    # open file and sepate values 
    with open(input_file, 'r') as i:
        for line in i:
            count = count + 1
            if count > 1:
                sepatated_values = line.split(",")
                
                sku = sepatated_values[3]
                price = sepatated_values[4]
                ondemandpris = sepatated_values[5]
            
                try: 
                    article = Article.objects.get(sku_number=sku)
                    print article
                    article.price = price                
                    article.ondemand_cost = ondemandpris
                    article.save()
                except: 
                    print "no article"
                
    return HttpResponse(status=200)

@login_required
def articlecostindex(request):
    artCost = ArticleCost.objects.all()


    return render_to_response('variation/articlecostindex.html',
                             {'artCost': artCost,

                              },
                             context_instance=RequestContext(request))