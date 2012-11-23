# cart/api.py
from tastypie import fields, utils
from tastypie.resources import ModelResource, Resource
from tastypie.api import Api #, CartItemResource

from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

from products.api import ArticleResource, PatternResource, ColorResource, SizeResource

from models import CartItem, Cart



class CartResource(ModelResource):
    #cartitems = fields.ForeignKey('cart.api.CartItemResource', attribute='cartitem', related_name="cartitem", full = True)

    class Meta:
        queryset = Cart.objects.all()
        resource_name = 'cart'
        authorization = DjangoAuthorization()
        authentication = Authentication()


    def dehydrate(self, bundle):
        cartid = bundle.obj.key
        cart1 = Cart.objects.get(key = cartid)
        list = CartItem.objects.filter(cart_id = cart1)
        main = []
        i = 1
        for l in list:
            dict = {'article':l.article.name, 'price':l.article.price, 'pattern':l.pattern.name, 'color':l.color.name, 'size':l.size.name }
            main = dict #.append(dict)
            print main
            i = i + 1

        bundle.data = main
        return bundle

class CartItemResource(ModelResource):
    cart_id = fields.ToOneField(CartResource, 'cart_id', full=True)
    article = fields.ToOneField(ArticleResource, 'article', full=True)
    color = fields.ToOneField(ColorResource, 'color', full=True)
    pattern = fields.ToOneField(PatternResource, 'pattern', full=True)
    size = fields.ToOneField(SizeResource, 'size', full=True)

    class Meta:
        queryset = CartItem.objects.all()
        resource_name = 'cartitem'
        authorization = DjangoAuthorization()
        authentication = Authentication()
