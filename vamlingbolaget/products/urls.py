from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'index'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    url(r'^patternandcolor/$', 'patternandcolor'),
    url(r'^products/type/(?P<name>[a-zA-Z0-9_.-]+)/$', 'category'),
    url(r'^products/quality/(?P<name>[a-zA-Z0-9_.-]+)/$', 'quality')
)