from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
    url(r'^show/(?P<key>[a-zA-Z0-9_.-]+)/$', 'showcart'),
    url(r'^addtocart/$', 'addtocart'),
)
