# cart/api.py
from tastypie import fields, utils
from tastypie.resources import ModelResource, Resource

from tastypie.api import Api #, CartItemResource

from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from products.api import ArticleResource, PatternResource, ColorResource, SizeResource

from models import CartItem

class CartItemResource(ModelResource):
    article = fields.ToOneField(ArticleResource, 'article', full=True)
    color = fields.ToOneField(ColorResource, 'color', full=True)
    pattern = fields.ToOneField(PatternResource, 'pattern', full=True)
    size = fields.ToOneField(SizeResource, 'size', full=True)

    class Meta:
        queryset = CartItem.objects.all()
        resource_name = 'cartitem'
        authorization = DjangoAuthorization()
        authentication = Authentication()