from django import template
from django.templatetags.static import register
from products.models import Quality, Type, Category

register = template.Library()

#@register.tag(name='shop_menu')
def shop_menu(context):
    qualities = Quality.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    types = Type.objects.filter(active=True)

    return { 'qualities': qualities, 'categories': categories, 'types': types }

register.inclusion_tag('variation/shop_menu.html', takes_context = True)(shop_menu)

#@register.tag(name='extra_lang')
def extra_lang(context):
    lang = 'se'
    wordlist = ['hus', 'katt']

    return { 'lang': lang, 'wordlist': wordlist }

register.inclusion_tag('lang.html', takes_context = True)(extra_lang)

