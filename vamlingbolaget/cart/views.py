from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Cart, CartItem
from django.http import HttpResponse
from products.models import Article, Color, Pattern, Size
import random
from django.core import urlresolvers
from models import CartItem

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from forms import CartForm
import json

CART_ID_SESSION_KEY = 'cart_id'


def addtocart(request):
    if request.method == 'POST':
        request_data = request.POST

        d = request_data
        sku = d['article_sku']
        article_db = Article.objects.get(sku_number = sku)
        color = d['color']
        color_db = Color.objects.get(order=color)

        pattern = d['pattern']
        pattern_db = Pattern.objects.get(order=pattern)

        size = d['size']
        size_db = Size.objects.get(pk=1) #TODO
        quantity = d['quantity']
        cart = Cart()
        article_in_cart = False

        """
        cart_article = get_cart_items(request)
        for cart_item in cart_article:
            if (cart_item.article.id == cart_article.id): #TODO add color and pattern and check
                cart_item.augment_quantity(quantity)
                article_in_cart = True

            if not article_in_cart:
        """

        cartitem = CartItem()
        cartitem.article = article_db
        cartitem.pattern = pattern_db
        cartitem.size = size_db
        cartitem.color = color_db

        cartitem.quantity = quantity
        cartitem.cart_id = _cart_id(request)
        print cartitem.cart_id
        cartitem.save()

    returnjson = {
            'cartitem': {
                'sku' : sku,
                'color': color,
                'pattern': pattern,
                'size': size,
                'quantity': quantity
            },
            'message': { 'msg' : 'listan uppdaterad'  }
        }


    return_data = json.dumps(returnjson)

    response = HttpResponse(return_data, mimetype="application/json")
    return response

def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

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


def showcart(request, key):
    cartitems = CartItem.objects.filter(cart_id=key)
    print key

    return render_to_response('cart/show_cart.html',
        {'cartitems': cartitems,},

        context_instance=RequestContext(request))

