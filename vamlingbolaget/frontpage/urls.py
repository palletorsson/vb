from django.conf.urls import patterns, include, url

urlpatterns = patterns('frontpage.views',
    url(r'test/$', 'first_page_b'),
    url(r'index/(?P<opt>[a-zA-Z0-9_.-]+)/$', 'first_page_opt'),
    url(r'^$', 'first_page_b'),
)


