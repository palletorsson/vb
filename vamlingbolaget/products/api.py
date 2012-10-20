# cart/api.py
from tastypie import fields, utils
from tastypie.resources import ModelResource, Resource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from models import Article, Color

class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
        authorization = DjangoAuthorization()
        authentication = Authentication()

class ColorResource(ModelResource):
    class Meta:
        queryset = Color.objects.all()
        resource_name = 'color'
        authorization = DjangoAuthorization()
        authentication = Authentication()
