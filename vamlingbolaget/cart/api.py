# cart/api.py
from tastypie.resources import ModelResource, fields, utils

from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from cart.models import CartItem
from products.models import Article

class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'

class CartItemResource(ModelResource):

    #articles = fields.ToManyField('ArticleResource', 'article', related_name='article')

    class Meta:
        queryset = CartItem.objects.all()
        resource_name = 'cartitem'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = Authentication()
	#excludes ['']
	