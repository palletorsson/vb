from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'index'),
    url(r'(?P<slug>[a-zA-Z0-9_.-]+)/$', 'detail'),

)
