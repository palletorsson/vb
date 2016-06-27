from django.conf.urls import patterns, url

urlpatterns = patterns('logger.views',
    url(r'^$', 'ShowAllLogging'),
    url(r'(?P<logger_id>[a-zA-Z0-9_.-]+)/$', 'ShowLog'),   
)


