from django import template
from django.templatetags.static import register
from blog.models import Post

register = template.Library()

#@register.inclusion_tag('base.html')
def show_news():
    news = Post.objects.filter(active=True, blog=2).order_by('-publish_at')[:2]

    return {'news': news}

register.inclusion_tag('blog/news_list.html')(show_news)
