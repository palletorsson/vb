# cart/api.py
from tastypie.resources import ModelResource
from cart.models import CartItem
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication


class CartItemResource(ModelResource):
    class Meta:
        queryset = CartItem.objects.all()
        resource_name = 'cartitem'
        #list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = Authentication()