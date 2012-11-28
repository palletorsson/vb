from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Page

def detail(request, slug):
    page = Page.objects.get(url=slug)
    return render_to_response('page/detail.html', {
        'post': page
    }, context_instance=RequestContext(request))

