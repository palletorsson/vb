from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
    url(r'^show/$', 'showcart'),
    url(r'^addtocart/$', 'addtocart'),
    url(r'^removefromcart/$', 'removefromcart'),
)
