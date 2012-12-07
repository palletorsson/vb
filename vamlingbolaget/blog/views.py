from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Blog, Post, New

def index(request):
    posts = Post.objects.filter(active=True)
    return render_to_response('blog/index.html', {
        'posts': posts,
    }, context_instance=RequestContext(request))
    
def detail(request, slug):
    post = get_object_or_404(Post, active=True, slug=slug)
    return render_to_response('blog/detail.html', {
        'post': post
    }, context_instance=RequestContext(request))
