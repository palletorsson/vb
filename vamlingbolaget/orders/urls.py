from django.conf.urls import patterns, url

urlpatterns = patterns('orders.views',
    url(r'^$', 'ShowOrders'),
    url(r'orders/(?P<stage>[a-zA-Z0-9_.-]+)/$', 'ShowOrders'),
    url(r'order/(?P<order_id>[a-zA-Z0-9_.-]+)/$', 'ShowOrder'),
    url(r'order/action/(?P<todo>[a-zA-Z0-9_.-]+)/(?P<stage>[a-zA-Z0-9_.-]+)/(?P<order_number>[a-zA-Z0-9_.-]+)/$', 'OrderAction'),
    url(r'order/action/(?P<todo>[a-zA-Z0-9_.-]+)/(?P<stage>[a-zA-Z0-9_.-]+)/(?P<order_number>[a-zA-Z0-9_.-]+)/(?P<send_type>[a-zA-Z0-9_.-]+)/$', 'OrderAction'),
    url(r'loadship/(?P<id>[a-zA-Z0-9_.-]+)/$', 'loadShipment'),
)


