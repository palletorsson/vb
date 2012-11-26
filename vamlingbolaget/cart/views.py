from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Cart, CartItem
from django.http import HttpResponse
from products.models import Article, Color, Pattern, Size, Quality
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
        sku = int(d['article_sku'])
        article_db = Article.objects.get(sku_number = sku)
        color = d['color']
        color_db = Color.objects.get(order=color)
        pattern = d['pattern']
        pattern_db = Pattern.objects.get(order=pattern)
        size = d['size']
        size_db = Size.objects.get(pk=size)
        quantity = int(d['quantity'])
        cartitem_id = int(d['cartitem_id'])
        item_in_cart = False

        if not item_in_cart:
            cart_id = _cart_id(request)
            cart, created = Cart.objects.get_or_create(key = cart_id)
            cart.save()
            if (cartitem_id == -1):
                cartitem = CartItem.objects.create(cart_id = cart)
            else:
                cartitem, created = CartItem.objects.get_or_create(pk = cartitem_id)
            cartitem.article = article_db
            cartitem.pattern = pattern_db
            cartitem.size = size_db
            cartitem.color = color_db
            cartitem.quantity = quantity
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
    handling  = 40
    for item in cartitems:
        totalprice += item.article.price * item.quantity
        totalitems += item.quantity
    totalprice = totalprice + handling
    print totalprice

    return render_to_response('cart/show_cart.html',
        {'cartitems': cartitems,
         'handling': handling,
         'totalprice': totalprice,
         'totalitems':totalitems,},

        context_instance=RequestContext(request))

def editcartitem(request, key):
    cartitem = CartItem.objects.get(pk=key)
    colors = Color.objects.all()
    patterns = Pattern.objects.all()
    sizes = Size.objects.all()
    qualities = Quality.objects.all()
    return render_to_response('cart/detail.html',
        {'cartitem': cartitem,
         'colors': colors,
         'patterns': patterns,
         'sizes': sizes,
         'qualities': qualities,
         },
        context_instance=RequestContext(request))


def removefromcart(request, key):
    cartitem = CartItem.objects.get(pk = key)
    mycart = cartitem.cart_id
    cartitem.delete()
    cart = Cart.objects.get(key=mycart)
    cartitems = cart.cartitem_set.all()
    print cartitems
    totalprice = 0
    totalitems = 0
    for item in cartitems:
        totalprice += item.article.price * item.quantity
        totalitems += item.quantity
    print totalprice

    return_data = json.dumps({'totalprice':totalprice, 'totalitems':totalitems})
    print cartitem.pk
    response = HttpResponse(return_data, mimetype="application/json")
    return response
