from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Blog, Post, New

def index(request):
    posts = Post.objects.filter(active=True)
    news = New.objects.filter(active=True)[:2]

    return render_to_response('blog/index.html', {
        'posts': posts,
        'news': news
    }, context_instance=RequestContext(request))
    
def detail(request, slug):
    post = get_object_or_404(Post, active=True, slug=slug)
    print post
    return render_to_response('blog/detail.html', {
        'post': post
    }, context_instance=RequestContext(request))
