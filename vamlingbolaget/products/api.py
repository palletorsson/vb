# cart/api.py
from tastypie import fields, utils
from tastypie.resources import ModelResource, Resource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from models import Article, Pattern, Color, Size

class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'articles'
        authorization = DjangoAuthorization()
        authentication = Authentication()

class ColorResource(ModelResource):
    class Meta:
        queryset = Color.objects.all()
        resource_name = 'colors'
        authorization = DjangoAuthorization()
        authentication = Authentication()

class PatternResource(ModelResource):
    class Meta:
        queryset = Pattern.objects.all()
        resource_name = 'pattern'
        authorization = DjangoAuthorization()
        authentication = Authentication()

class SizeResource(ModelResource):
        class Meta:
            queryset = Size.objects.all()
            resource_name = 'size'
            authorization = DjangoAuthorization()
            authentication = Authentication()