# cart/api.py
from tastypie import fields, utils
from tastypie.resources import ModelResource, Resource
from tastypie.api import Api #, CartItemResource

from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from products.api import ArticleResource, PatternResource, ColorResource, SizeResource

from models import CartItem, Cart

class CartResource(ModelResource):
    class Meta:
        queryset = Cart.objects.all()[:1]
        resource_name = 'cart'
        authorization = DjangoAuthorization()
        authentication = Authentication()


class CartItemResource(ModelResource):
    article = fields.ToOneField(ArticleResource, 'article', full=True)
    color = fields.ToOneField(ColorResource, 'color', full=True)
    pattern = fields.ToOneField(PatternResource, 'pattern', full=True)
    size = fields.ToOneField(SizeResource, 'size', full=True)

    class Meta:
        queryset = CartItem.objects.all()[:2]
        resource_name = 'cartitem'
        authorization = DjangoAuthorization()
        authentication = Authentication()
