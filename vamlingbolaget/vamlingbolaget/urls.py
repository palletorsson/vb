from django.conf.urls import patterns, include, url
from django.conf import settings
from filebrowser.sites import site

from tastypie.api import Api

from cart.api import CartResource, CartItemResource
from products.api import ArticleResource, ColorResource, PatternResource, SizeResource

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(CartResource())
v1_api.register(CartItemResource())
v1_api.register(ArticleResource())
v1_api.register(ColorResource())
v1_api.register(PatternResource())
v1_api.register(SizeResource())


urlpatterns = patterns('',

    url(r'^$', 'frontpage.views.first_page', name='index'),
    url(r'^products/', include('products.urls')),
    url(r'^patternandcolor/$', 'products.views.pattern_and_color'),
    url(r'^galleries/$', 'gallery.views.show_galleries'),
    url(r'^gallery/(?P<key>[a-zA-Z0-9_.-]+)/$', 'gallery.views.show_gallery'),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^cart/', include('cart.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^news/', include('blog.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^photologue/', include('photologue.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(v1_api.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n'), name='i18n'),

)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^theme/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
