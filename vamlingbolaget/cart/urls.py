from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
    url(r'^s_how/$', 'showcart_b', name='showcart_b'),
    url(r'^show/$', 'showcart', name='showcart_b'),
    url(r'^showbyid/(?P<session_id>[a-zA-Z0-9_.-]+)/$', 'showcartBySessionId', name='showcart'),
    url(r'^addtocart/$', 'addtocart'),
    url(r'^remove/(?P<pk>[a-zA-Z0-9_.-]+)/(?P<type>[a-zA-Z0-9_.-]+)/$', 'removefromcart',  name='removefromcart'),
    url(r'^voucher/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'voucher',  name='voucher'),
    url(r'^edititem/(?P<key>[a-zA-Z0-9_.-]+)/$', 'editcartitem',  name='editcartitem'),
    url(r'^addrea/$', 'add_rea'),
    url(r'^admin_customer/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 'customer_email'),
    url(r'^addbargain/$', 'add_bargain'),
    
)
