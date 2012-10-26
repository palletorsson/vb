from django.conf.urls import patterns, include, url
from django.conf import settings

from tastypie.api import Api

from cart.api import CartItemResource
from products.api import ArticleResource, ColorResource, PatternResource, SizeResource

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')


v1_api.register(CartItemResource())
v1_api.register(ArticleResource())
v1_api.register(ColorResource())
v1_api.register(PatternResource())
v1_api.register(SizeResource())

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(v1_api.urls)),

)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
