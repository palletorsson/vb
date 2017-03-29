from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'index'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    url(r'^rea/$', 'reaindex'),
    url(r'^rea/size/(?P<key>[a-zA-Z0-9_.-]+)/$', 'rea_by_size'),
    url(r'^rea/(?P<pk>\d+)/$', 'readetail'),
    url(r'^type/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_type'),
    url(r'^quality/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_quality'),
    url(r'^bargain/$', 'bargain', name='bargains'),
    url(r'^bargain/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'bargain_detail', name='bargain_detail'),
    url(r'^patternandcolortest/$', 'colorpatterntest'),

)
