from django import template
from django.templatetags.static import register
from blog.models import New

register = template.Library()

#@register.inclusion_tag('base.html')
def show_news():
    news = New.objects.filter(active=True).order_by('-publish_at')[:2]
    print news
    return {'news': news}

register.tag('show_news', show_news)