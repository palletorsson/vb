# cart/api.py
from tastypie.resources import ModelResource
from cart.models import CartItem


class CartItemResource(ModelResource):
    class Meta:
        queryset = CartItem.objects.all()
        resource_name = 'cartitem'
        list_allowed_methods = ['get', 'post']
