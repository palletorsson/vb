from django.conf.urls import patterns, include, url

urlpatterns = patterns('project.views',
    url(r'tranpo/$', 'transtest'),
    url(r'trans/(?P<string>[a-zA-Z0-9_.-]+)/(?P<lang>[a-zA-Z0-9_.-]+)/$', 'transString'),
    url(r'fulltrans/(?P<lang>[a-zA-Z0-9_.-]+)/(?P<model>[a-zA-Z0-9_.-]+)$', 'full_tranlation'),
    url(r'(?P<pk>[a-zA-Z0-9_.-]+)/$', 'detail'),
    url(r'^$', 'index'),
)