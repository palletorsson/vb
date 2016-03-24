from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import Campaign, Media, File, Kanban
import json
import contextlib
import os
import time



def index(request):
    campaigns = Campaign.objects.filter(status="A")
    campaigns_expired = Campaign.objects.filter(status="E")
    campaigns_public = Campaign.objects.filter(status="P")

    return render_to_response('campaigns/first_page.html',
							{'campaigns': campaigns, 
                             'campaigns_expired': campaigns_expired, 
                             'campaigns_public': campaigns_public, 
							},
							context_instance=RequestContext(request))

def detail(request, pk):
    temp_int = 1
    campaign = Campaign.objects.get(pk=pk)
    files = File.objects.filter(campaign=campaign)
    media = Media.objects.filter(campaign=campaign)
    kanban = Kanban.objects.filter(campaign=campaign)
       
    return render_to_response('campaigns/detail.html',
							{'campaign': campaign,
                             'files': files, 
                             'media': media,
                             'kanban': kanban,
							},
							context_instance=RequestContext(request))



