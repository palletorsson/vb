from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Cart, CartItem
from django.http import HttpResponse
from products.models import Article, Color, Pattern, Size
import random
from django.core import urlresolvers
from models import CartItem
from django.core.urlresolvers import reverse

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from forms import CartForm
import json

CART_ID_SESSION_KEY = 'cart_id'


def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id

def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY,'') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

def augment_quantity(self, quantity):
    self.quantity = self.quantity + int(quantity)
    self.save()


def addtocart(request):
    if request.method == 'POST':

        d = request.POST
        sku = d['article_sku']
        print sku
        article_db = Article.objects.get(sku_number = sku)
        print article_db
        color = d['color']
        print color
        color_db = Color.objects.get(order=color)

        pattern = d['pattern']
        pattern_db = Pattern.objects.get(order=pattern)

        size = d['size']
        size_db = Size.objects.get(pk=size)

        quantity = d['quantity']
        print "---------1---"
        #cart_items = get_cart_items(request)
        item_in_cart = False

        """
        for item in cart_items:
            if (item.article.pk == article_db.pk and item.color.pk == color_db.pk and item.pattern.pk == pattern_db.pk):
                quantity = int(quantity)
                quantity = quantity + int(item.quantity)
                item.quantity = quantity
                item.save()
                item_in_cart = True
         """

        print "---------2---"
        if not item_in_cart:
            cart_id = _cart_id(request) #skapar nytt cart
            cart, created = Cart.objects.get_or_create(key = cart_id)
            cart.save()
            print cart.key
            print request.session[CART_ID_SESSION_KEY]
            cartitem = CartItem.objects.create(cart_id = cart)
            print cartitem.cart_id.key
            cartitem.article = article_db
            cartitem.pattern = pattern_db
            cartitem.size = size_db
            cartitem.color = color_db
            cartitem.quantity = quantity
            print cartitem
            cartitem.save()

        returnjson = {
            'cartitem': {
                'article': article_db.name,
                'sku' : sku,
                'color': color_db.name,
                'pattern': pattern_db.name,
                'size': size_db.name,
                'quantity': quantity,
                 },
            'message': { 'msg' : 'Du la till: '  }
        }


    return_data = json.dumps(returnjson)

    response = HttpResponse(return_data, mimetype="application/json")
    return response


def show_product(request, article_slug):
    a = get_object_or_404(Article, slug=article_slug)

    if request.method == 'POST':
        data= request.POST.copy()
        form = CartForm(request, data)

        if form.is_valid():
            #add to cart and redirect to cart page
            Cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                url = urlresolvers.reverse('show_cart')
                return HttpResponseRedirect(url)
            else:
                form = CartForm(request=request, label_suffix=':')

            request.session.set_test_cookie()
            return render_to_response("variation/detail.html", locals(), context_instance=RequestContext(request))


def showcart(request):
    key = _cart_id(request)
    cart = Cart.objects.get(key=key)
    cartitems = cart.cartitem_set.all()
    print cartitems
    totalprice = 0
    totalitems = 0
    for item in cartitems:
        totalprice += item.article.price * item.quantity
        totalitems += item.quantity
    print totalprice

    return render_to_response('cart/show_cart.html',
        {'cartitems': cartitems,
         'totalprice': totalprice,
         'totalitems':totalitems,},

        context_instance=RequestContext(request))

def removefromcart(request, key):
    cartitem = CartItem.objects.get(pk=key)
    cartitem.delete()
    return HttpResponse('ok')
