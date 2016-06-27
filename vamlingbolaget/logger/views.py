from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import LogItem


def keepLog(request, title, log_level, ip, session_key='', json_dump=''): 
    log = LogItem(title=title, log_level=log_level, ip=ip, session_key=session_key, json_dump=json_dump)
    log.save() 


def ShowAllLogging(request): 
    logs = LogItem.objects.all().order_by('-date_added')[:100]

    return render_to_response('log/logs.html', {
        'logs': logs,
    }, context_instance=RequestContext(request))

def ShowLog(request, logger_id):

    log = LogItem.objects.get(pk=logger_id)
 
    return render_to_response('log/log.html', {
        'log': log,
    }, context_instance=RequestContext(request))
