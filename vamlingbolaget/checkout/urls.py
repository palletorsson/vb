from django.conf.urls import patterns, url

urlpatterns = patterns('checkout.views',
    url(r'^$', 'checkout'),
    url(r'_/$', 'checkout_b'),
    url(r'thanks/', 'thanks'),
    url(r'success/', 'success'),
    url(r'cancel/', 'cancel'),
    url(r'payexCallback/', 'payexCallback'),
    url(r'fortnox/$', 'fortnox'),
    url(r'reaadmin/(?P<limit>[a-zA-Z0-9_.-]+)/$', 'rea_admin_views'),
    url(r'reatotal/(?P<limit>[a-zA-Z0-9_.-]+)/$', 'rea_admin_total'),
    url(r'admin/(?P<limit>[a-zA-Z0-9_.-]+)/$', 'admin_view'),
    url(r'pacsoft/$', 'pacsoft'),
    url(r'tests/$', 'testingRemoveStock'),
    url(r'seekorders/(?P<key>[a-zA-Z0-9_.-]+)/$', 'readOrders'),
    url(r'consumorder/(?P<order_id>[a-zA-Z0-9_.-]+)/(?P<force>[a-zA-Z0-9_.-]+)/$', 'consumOrder'),
    url(r'consumordercheck/(?P<order_id>[a-zA-Z0-9_.-]+)/$', 'getOrderbyOrderNumerAndCheck'),
    url(r'klhanks/$', 'klarna_thanks'),
    url(r'klarnatestid/$', 'testconfirmklarnahtml'),
    url(r'push_klar/(?P<klarna_id>[a-zA-Z0-9_.-]+)/$', 'klarna_push'),
    url(r'klarna/$', 'checkout'),

)

