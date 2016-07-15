from django.conf.urls import patterns, include, url

urlpatterns = patterns('gallery.views',
	url(r'^(?P<key>[a-zA-Z0-9_.-]+)/$', 'show_gallery'), 
    url(r'^import/$', 'CsvGallery'),
)



