from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
    url(r'^show/$', 'showcart', name='showcart'),
    url(r'^addtocart/$', 'addtocart'),
    url(r'^removefromcart/(?P<key>[a-zA-Z0-9_.-]+)/$', 'removefromcart',  name='removefromcart'),
)
