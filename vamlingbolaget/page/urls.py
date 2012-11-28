from django.conf.urls import patterns, url
from views import detail

urlpatterns = patterns('',
    url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', detail),
)

