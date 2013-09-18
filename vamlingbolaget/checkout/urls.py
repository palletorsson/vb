from django.conf.urls import patterns, url

urlpatterns = patterns('checkout.views',
    url(r'^$', 'checkout'),
    url(r'test/', 'checkout_test'),
    url(r'thanks/', 'thanks'),
    url(r'success/', 'success'),
    url(r'cancel/', 'cancel'),
)


