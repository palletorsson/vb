from models import CartItem
from products.models import Article
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import decimal
import random
from forms import CartForm
import json

CART_ID_SESSION_KEY = 'cart_id'

def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY,'') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id

def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

def add_to_cart(request):
    data = request.POST['json']
    data = json.loads(data)
    article = data['article']
    pattern = data['pattern']
    color = data['color']
    size = data['size']
    quantity = data['quantity']
    cart_article = get_cart_items(request)
    for cart_item in cart_article:
        if (cart_item.article.id == article.id): #TODO add color and pattern and check
            cart_item.augment_quantity(quantity)
            article_in_cart = True
        if not article_in_cart:
            cartitem = CartItem.objects.create()
            cartitem.article = article
            cartitem.pattern = pattern
            cartitem.size = size
            cartitem.color = color
            cartitem.quantity = quantity
            cartitem.cart_id = _cart_id(request)
            cartitem.save()
            # returns the total number of items in the user's cart

def cart_distinct_item_count(request):
    return get_cart_items(request).count()

