from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
    url(r'^show/$', 'showcart', name='showcart'),
    url(r'^addtocart/$', 'addtocart'),
    url(r'^remove/(?P<pk>[a-zA-Z0-9_.-]+)/(?P<type>[a-zA-Z0-9_.-]+)/$', 'removefromcart',  name='removefromcart'),
    url(r'^edititem/(?P<key>[a-zA-Z0-9_.-]+)/$', 'editcartitem',  name='editcartitem'),
    url(r'^addbargain/$', 'add_bargain'),
)
