from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'fullindex_c'),
    url(r'^fullcut/$', 'fullindexarticle'),
    url(r'^test_f/$', 'fullindex_b'),
    url(r'^full/$', 'fullindex_c'),
    url(r'^preview/$', 'fulllastindex'),
    url(r'^cod/$', 'codwizard'),
    url(r'^cut/$', 'fullindex_c'),
    url(r'^test_cut/$', 'reacut_c'),
    url(r'^fullindexlist/$', 'fullindexlist'),
    url(r'^full/quality/(?P<quality>[a-zA-Z0-9_.-]+)/$', 'fullindexQuality'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    #url(r'^rea/$', 'reaindex'),
    url(r'^rea/$', 'reareact_b'),
    url(r'^rea_b/$', 'reareact_b'),
    url(r'^reajson/$', 'jsonReaindex'),
    url(r'^codartjson/(?P<category>[a-zA-Z0-9_.-]+)/$', 'cutondemandApi'),
    url(r'^codartjsonsingle/(?P<sku_number>[a-zA-Z0-9_.-]+)/$', 'cutondemandApiSingle'),
    url(r'^rea/size/(?P<key>[a-zA-Z0-9_.-]+)/$', 'rea_by_size'),
    url(r'^rea/type/(?P<key>[a-zA-Z0-9_.-]+)/$', 'rea_by_type'),
    url(r'^rea/(?P<pk>\d+)/$', 'reaindex'), #'readetail'
    url(r'^reaart/(?P<pk>\d+)/$', 'readetail_d'), #'readetail_d'
    url(r'^type/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_type'),
    url(r'^cat/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_cat'),
    url(r'^ct/(?P<cat>[a-zA-Z0-9_.-]+)/(?P<thetype>[a-zA-Z0-9_.-]+)/$', 'by_cat_type'),
    url(r'^qt/(?P<cat>[a-zA-Z0-9_.-]+)/(?P<q>[a-zA-Z0-9_.-]+)/$', 'by_cat_q'),
    url(r'^product/(?P<key>[a-zA-Z0-9_.-]+)/$', 'product_api'),
    url(r'^quality/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_quality'),
    #url(r'^bargain/$', 'bargain', name='bargains'),
    #url(r'^bargain/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'bargain_detail', name='bargain_detail'),
    url(r'^patternandcolor/$', 'colorpatterntest'),
    url(r'^articles_admin/$', 'allArticles'),
    url(r'^articles/$', 'articleindex'),
    url(r'^articles/article/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'artdetail'),
    url(r'^fullvariation/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'fulldetail'),
    url(r'^fulldetail/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'fulldetail_b'),
    url(r'^vardetail/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'fulldetail_v'),
    url(r'^article/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'articleDetail'),
    url(r'^allart_admin/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'allArt'),
    url(r'^allfullart_admin/(?P<quality>[a-zA-Z0-9_.-]+)/$', 'allFullArt'),
    url(r'^duplicates/(?P<remove>[a-zA-Z0-9_.-]+)/$', 'variationduplicates'),
    #url(r'^allart_rea/$', 'reaindex'), #'allreaArt'
    #url(r'^articles/$', 'articleList'),
    url(r'^articlescsv/$', 'articlesCsv'),

    url(r'^readcsv/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'readCsv'),
    url(r'^readcsvman/(?P<what>[a-zA-Z0-9_.-]+)/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)/$', 'readCsvManchester'),
    url(r'^checkcsv/$', 'readCsvOnlyCheck'),
    url(r'^ordercsv/$', 'orderCsv'),
    url(r'^setdiscount/(?P<what>[a-zA-Z0-9_.-]+)/$', 'setDiscount'),
    url(r'^setnewprice/$', 'setPriceFromlist'),
    url(r'^setstock/$', 'setfullstockCsv'),
    url(r'^setactivenon/$', 'setActiveNon'),
    url(r'^setfulltrue/$', 'setfullTrue'),

    url(r'^ordercsv/$', 'orderfromCsv'),
    url(r'^delfromcsv/(?P<start_at>[a-zA-Z0-9_.-]+)/(?P<end_at>[a-zA-Z0-9_.-]+)$', 'removeCsv'),
    url(r'^removecolor/(?P<color>[a-zA-Z0-9_.-]+)/(?P<act>[a-zA-Z0-9_.-]+)$', 'removeByColor'),
    url(r'^articlestrans/$', 'articlesTranferToFortnox'),
    url(r'^article_stock/(?P<sku_num>[a-zA-Z0-9_.-]+)/(?P<stock>[a-zA-Z0-9_.-]+)/$', 'articleUpdateStock'),
)
