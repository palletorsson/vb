# cart/api.py
from tastypie import fields, utils
from tastypie.resources import ModelResource, Resource

from tastypie.api import Api #, CartItemResource


from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from products.api import ArticleResource, ColorResource

from models import CartItem

class CartItemResource(ModelResource):
    article = fields.ToOneField(ArticleResource, 'article')
    color = fields.ToOneField(ColorResource, 'color')

    class Meta:
        queryset = CartItem.objects.all()
        resource_name = 'cartitem'
        authorization = DjangoAuthorization()
        authentication = Authentication()

	