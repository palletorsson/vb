from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Frontpage
from blog.models import Post


def first_page(request):
    frontpage = Frontpage.objects.get(pk=1)
    news = Post.objects.all()

    return render_to_response('frontpage/first_page.html',
        {'frontpage': frontpage,
         'news': news,},
        context_instance=RequestContext(request))
