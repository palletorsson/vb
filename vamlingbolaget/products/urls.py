from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'index'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    url(r'^type/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_type'),
    url(r'^quality/(?P<key>[a-zA-Z0-9_.-]+)/$', 'by_quality'),
    url(r'^bargain/$', 'bargain'),
    url(r'^bargain/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'bargain_detail'),

)