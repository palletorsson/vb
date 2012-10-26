from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from blog.models import Blog, Post

def blog_index(request):
    blogs = Blog.objects.filter(active=True)
    
    return render_to_response('index.html', {
        'blogs': blogs 
    }, context_instance=RequestContext(request))
    
def blog(request, slug):
    blog = get_object_or_404(Blog, active=True, slug=slug)
    