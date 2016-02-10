from django.conf.urls import patterns, url

urlpatterns = patterns('checkout.views',
    url(r'^$', 'checkout'),
    url(r'thanks/', 'thanks'),
    url(r'success/', 'success'),
    url(r'cancel/', 'cancel'),
    url(r'payexCallback/', 'payexCallback'),
    url(r'fortnox/$', 'fortnox'),
    url(r'admin/$', 'admin_view'),
    url(r'pacsoft/$', 'pacsoft'),
    url(r'tests/$', 'testingRemoveStock'),
)


