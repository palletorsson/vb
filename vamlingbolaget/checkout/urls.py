from django.conf.urls import patterns, url

urlpatterns = patterns('checkout.views',
    url(r'^$', 'checkout'),
    url(r'thanks/', 'thanks'),
)


