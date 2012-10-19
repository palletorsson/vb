from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api
from cart.api import CartItemResource

admin.autodiscover()

cart_resource = CartItemResource()
cartApi = Api(api_name = 'cart') #global tastypieklass, till backbone tror vi....
cartApi.register(CartItemResource())#var ska vara med

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(cartApi.urls)),
)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
