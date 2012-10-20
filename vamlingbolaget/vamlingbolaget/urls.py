from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api

from cart.api import CartItemResource
from products.api import ArticleResource, ColorResource, PatternResource, SizeResource

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

pattern_resource = PatternResource()
patternApi = Api(api_name = 'pattern')
patternApi.register(PatternResource())

size_resource = SizeResource()
sizeApi = Api(api_name = 'size')
sizeApi.register(SizeResource())

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/cart/', include(cartApi.urls)),
    url(r'^api/products/', include(articleApi.urls)),
    url(r'^api/colors/', include(colorApi.urls)),
    url(r'^api/pattern/', include(patternApi.urls)),
    url(r'^api/size/', include(sizeApi.urls)),
)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
