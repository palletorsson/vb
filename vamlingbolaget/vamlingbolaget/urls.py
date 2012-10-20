from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api

from cart.api import CartItemResource
from products.api import ArticleResource, ColorResource

admin.autodiscover()

cart_resource = CartItemResource()
cartApi = Api(api_name = 'cart')
cartApi.register(CartItemResource())

article_resource = ArticleResource()
articleApi = Api(api_name = 'articles')
articleApi.register(ArticleResource())

color_resource = ColorResource()
colorApi = Api(api_name = 'color')
colorApi.register(ColorResource())

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/cart/', include(cartApi.urls)),
    url(r'^api/products/', include(articleApi.urls)),
    url(r'^api/color/', include(colorApi.urls)),
)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
