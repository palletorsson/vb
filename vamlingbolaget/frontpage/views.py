from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Frontpage, FrontpageTheme, FrontpageExtended
from gallery.models import Gallery, Image
from blog.models import New
from products.models import Variation, Article, Pattern, Color

def first_page(request):
    frontpage, created = Frontpage.objects.get_or_create(pk=1)
    gallery = Gallery.objects.filter(status__display_on_index_page = True) 
    images = Image.objects.filter(gallery=gallery)
    news = New.objects.filter(active=True).order_by('-publish_at')[:2]
    features = FrontpageExtended.objects.filter(status='A', theme__title='rightNow').order_by('order')
    theme1 = FrontpageTheme.objects.filter(status='A').order_by('order')[:1]

    return render_to_response('frontpage/first_page_now.html',
        {'frontpage': frontpage,
         'gallery' : gallery,
         'images': images,
         'news': news,
         'features': features,
         'theme1': theme1
        },
        context_instance=RequestContext(request))

def first_page_b(request):
    frontpage, created = Frontpage.objects.get_or_create(pk=1)
    theme1 = FrontpageTheme.objects.filter(status='A').order_by('order')[:1]
    features = FrontpageExtended.objects.filter(status='A', theme__title='rightNow').order_by('order')
  

    return render_to_response('frontpage/first_page_b.html',
        {
            'frontpage': frontpage,
            'theme1': theme1,
            'features': features,
            'showtopmenu': True, 
            'language': True
        },
        context_instance=RequestContext(request))

def first_page_opt(request, opt):

    frontpage, created = Frontpage.objects.get_or_create(pk=1)
    gallery = Gallery.objects.filter(status__display_on_index_page = True) 
    images = Image.objects.filter(gallery=gallery)
    news = New.objects.filter(active=True).order_by('-publish_at')[:2]
    features = FrontpageExtended.objects.filter(status='A', theme__title=opt).order_by('order')
    theme1 = FrontpageTheme.objects.filter(status='A').order_by('order')[:1]
    print features
    for feature in features: 
        try: 
            heading_split = feature.heading.split("_")
            if int(heading_split[0]) > 1: 
                    article = Article.objects.get(sku_number=heading_split[0])
                    pattern = Pattern.objects.get(order=int(heading_split[2]))
                    color = Color.objects.get(order=heading_split[1])
                    variation = Variation.objects.get(article=article, pattern=pattern, color=color)
                    feature.heading = variation
                
        except: 
            pass
    return render_to_response('frontpage/first_page_now.html',
        {'frontpage': frontpage,
         'gallery' : gallery,
         'images': images,
         'news': news,
         'features': features,
         'theme1': theme1
        },
        context_instance=RequestContext(request))