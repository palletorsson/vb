from django.conf.urls import patterns, include, url
from django.conf import settings
from cart.api import CartItemResource
from django.contrib import admin
admin.autodiscover()

cart_resource = CartItemResource()

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(cart_resource.urls)),
)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
