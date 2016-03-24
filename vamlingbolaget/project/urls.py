from django.conf.urls import patterns, include, url

urlpatterns = patterns('project.views',
    url(r'^$', 'index'),
    url(r'(?P<pk>[a-zA-Z0-9_.-]+)/$', 'detail'),
)



