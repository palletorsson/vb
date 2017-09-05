from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'index'),
    url(r'^fullcut/$', 'fullindexarticle'),
    url(r'^full/$', 'fullindex'),
    url(r'^preview/$', 'fulllastindex'),
    url(r'^fullindexlist/$', 'fullindexlist'),
    url(r'^full/quality/(?P<quality>[a-zA-Z0-9_.-]+)/$', 'fullindexQuality'),
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
    url(r'^allart_admin/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'allArt'),
    url(r'^allfullart_admin/(?P<quality>[a-zA-Z0-9_.-]+)/$', 'allFullArt'),
    url(r'^duplicates/(?P<remove>[a-zA-Z0-9_.-]+)/$', 'variationduplicates'),   
    url(r'^allart_rea/$', 'allreaArt'),
    #url(r'^articles/$', 'articleList'),
    url(r'^articlescsv/$', 'articlesCsv'),
    url(r'^readcsv/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'readCsv'),
    url(r'^readcsvman/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'readCsvManchester'),
    url(r'^checkcsv/$', 'readCsvOnlyCheck'),
    url(r'^ordercsv/$', 'orderCsv'),
    url(r'^setdiscount/(?P<what>[a-zA-Z0-9_.-]+)/$', 'setDiscount'),
    url(r'^setnewprice/$', 'setPriceFromlist'),        
    url(r'^delfromcsv/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)$', 'removeCsv'),
    url(r'^removecolor/(?P<color>[a-zA-Z0-9_.-]+)/(?P<act>[a-zA-Z0-9_.-]+)$', 'removeByColor'),
    url(r'^articlestrans/$', 'articlesTranferToFortnox'),
    url(r'^article_stock/(?P<sku_num>[a-zA-Z0-9_.-]+)/(?P<stock>[a-zA-Z0-9_.-]+)/$', 'articleUpdateStock'),    
)
