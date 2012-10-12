from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from models import Variation

urlpatterns = patterns('products.views',
    url(r'^$', 'index'),
    url(r'^(?P<pk>\d+)/$', 'detail'),   
)