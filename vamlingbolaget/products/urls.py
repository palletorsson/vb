from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'index'),
    url(r'^full/$', 'fullindex'),
    url(r'^fullindexlist/$', 'fullindexlist'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    url(r'^rea/$', 'reaindex'),
    url(r'^rea/size/(?P<key>[a-zA-Z0-9_.-]+)/$', 'rea_by_size'),
    url(r'^rea/type/(?P<key>[a-zA-Z0-9_.-]+)/$', 'rea_by_type'),
    url(r'^rea/(?P<pk>\d+)/$', 'readetail'),
    url(r'^type/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_type'),
    url(r'^product/(?P<key>[a-zA-Z0-9_.-]+)/$', 'product_api'),
    url(r'^quality/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_quality'),
    #url(r'^bargain/$', 'bargain', name='bargains'),
    #url(r'^bargain/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'bargain_detail', name='bargain_detail'),
    url(r'^patternandcolortest/$', 'colorpatterntest'),
    url(r'^articles_admin/$', 'allArticles'),
    url(r'^articles/$', 'articleindex'),    
    url(r'^articles/article/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'artdetail'), 
    url(r'^fullvariation/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'fulldetail'), 
    url(r'^article/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'articleDetail'), 
    url(r'^allart_admin/$', 'allArt'),
    url(r'^allfullart_admin/$', 'allFullArt'),

    url(r'^allart_rea/$', 'allreaArt'),
    #url(r'^articles/$', 'articleList'),
    url(r'^articlescsv/$', 'articlesCsv'),
    url(r'^readcsv/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'readCsv'),
    url(r'^readcsvman/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'readCsvManchester'),
    url(r'^checkcsv/$', 'readCsvOnlyCheck'),
    url(r'^ordercsv/$', 'orderCsv'),
    url(r'^delfromcsv/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)$', 'removeCsv'),
    
    url(r'^articlestrans/$', 'articlesTranferToFortnox'),
    url(r'^article_stock/(?P<sku_num>[a-zA-Z0-9_.-]+)/(?P<stock>[a-zA-Z0-9_.-]+)/$', 'articleUpdateStock'),    
)
