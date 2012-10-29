from django.conf.urls import patterns, include, url
from django.conf import settings

from filebrowser.sites import site

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
    url(r'^$', include('products.urls')),
    url(r'^products/', include('products.urls')),

    url(r'^news/', include('blog.urls')),
    url(r'^tiny_mce/', include('tinymce.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(v1_api.urls)),

)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)


urlpatterns += patterns('',

    (r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
 { 'document_root': '/home/palle/Project/django/virtual_vb/vb/vamlingbolaget/tiny_mce/' }),


)
