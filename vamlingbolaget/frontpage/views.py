from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Frontpage
from gallery.models import Gallery
from blog.models import Post


def first_page(request):
    frontpage = Frontpage.objects.get(pk=1)
    gallery = Gallery.objects.get(status = 'I')
    images = gallery.image_set.all()
    news = Post.objects.all()

    return render_to_response('frontpage/first_page2.html',
        {'frontpage': frontpage,
         'images': images,
         'news': news,},
        context_instance=RequestContext(request))
