from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Cart, CartItem, BargainCartItem, VoucherCart
from django.http import HttpResponse
from products.models import Article, Color, Pattern, Size, Quality, Bargainbox
import random
from django.core import urlresolvers
from models import CartItem
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from forms import CartForm
import json
import pygeoip
from vamlingbolaget.settings import ROOT_DIR
import operator


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

def _rest_cart_id(request):
    request.session[CART_ID_SESSION_KEY] = ''

def _new_cart_id(request):
    request.session[CART_ID_SESSION_KEY] = _generate_cart_id()

def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

def augment_quantity(self, quantity):
    self.quantity = self.quantity + int(quantity)
    self.save()

def addtocart(request):
    if (request.method == 'POST'):
        d = request.POST
        sku = d['article_sku']
        article_db = Article.objects.get(sku_number = sku)

        color = d['color']
        pattern = d['pattern']
        color2 = int(d['color2'])
        print color2
        if(color2 == 0):
            pass
        else:
            color2 = d['color2']
            pattern2 = d['pattern2']

        size = d['size']
        quantity = int(d['quantity'])
        cartitem_id = int(d['cartitem_id'])
        add_or_edit = d['add_or_edit']

        cart_id = _cart_id(request)

        cart, created = Cart.objects.get_or_create(key = cart_id)
        cart.save()

        existing_cartitems = CartItem.objects.filter(cart=cart)

        update = False
        if (cartitem_id and add_or_edit == 'edit'):
            cartitem = CartItem.objects.get(pk=cartitem_id)
            cartitem.size = size
            cartitem.color = color
            cartitem.pattern = pattern
            if(color2 > 0):
                cartitem.color_2 = color2
                cartitem.pattern_2 = pattern2
            cartitem.quantity = quantity
            cartitem.save()
            msg = u'Du har andrat till: </br>'

        elif (existing_cartitems):
            for item in existing_cartitems:
                if (str(item.article.sku_number) == str(sku) and str(item.pattern) == str(pattern) and
                    str(item.color) == str(color) and str(item.size) == str(size)):
                    item.quantity = item.quantity + quantity
                    item.save()
                    msg = u'Du la till ytterligare %s %s och har nu: <br/>' %(quantity, article_db.name)
                    quantity = item.quantity
                    update = True
            if update != True:
                cartitem = CartItem.objects.create(cart = cart)
                cartitem.article = article_db
                cartitem.pattern = pattern
                if(color2 > 0):
                    cartitem.color_2 = color2
                    cartitem.pattern_2 = pattern2
                cartitem.size = size
                cartitem.color = color
                cartitem.quantity = quantity
                cartitem.save()
                msg = u'Du har lagt till: <br/>'

        else:
            cartitem = CartItem.objects.create(cart = cart)
            cartitem.article = article_db
            cartitem.pattern = pattern
            cartitem.size = size
            cartitem.color = color
            if(color2 > 0):
                cartitem.color_2 = color2
                cartitem.pattern_2 = pattern2
            cartitem.quantity = quantity
            cartitem.save()
            msg = u'Du har lagt till: <br/>'

        color_db = Color.objects.get(order=color)
        pattern_db = Pattern.objects.get(order=pattern)
        size_db = Size.objects.get(pk=size)

        if(color2 == 0):
            pass
        else:
            color_db2 = Color.objects.get(order = color2)
            pattern_db2 = Pattern.objects.get(order = pattern2)

        if(color2 > 0):
            returnjson = {
                    'cartitem': {
                        'article': article_db.name,
                        'sku' : sku,
                        'color': color_db.name,
                        'pattern': pattern_db.name,
                        'color': color_db.name,
                        'pattern': pattern_db.name,
                        'color2': color_db2.name,
                        'pattern2': pattern_db2.name,
                        'color': color_db.name,
                        'pattern': pattern_db.name,
                        'size': size_db.name,
                        'quantity': quantity,
                        },
                    'message': { 'msg' : msg  }
                }
        else:
            returnjson = {
                    'cartitem': {
                        'article': article_db.name,
                        'sku' : sku,
                        'color': color_db.name,
                        'pattern': pattern_db.name,
                        'color': color_db.name,
                        'pattern': pattern_db.name,
                        'size': size_db.name,
                        'quantity': quantity,
                        },
                    'message': { 'msg' : msg  }
                }

        return_data = json.dumps(returnjson)

    if request.method == 'GET':
        return_data = json.dumps({'msg' : 'nothing here'})

    response = HttpResponse(return_data, mimetype="application/json")
    return response

def add_bargain(request):
    if request.POST:
        d = request.POST
        item = d['item']
        bargain = Bargainbox.objects.get(pk=item)

        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(key = cart_id)
        cart.save()

        existing_bargainitems = BargainCartItem.objects.filter(cart=cart)
        print existing_bargainitems

        inbox = False

        for existingbargain in existing_bargainitems:
            if bargain.pk == existingbargain.bargain.pk:
                msg = u'Fyndet finns redan '
                inbox = True

        if inbox == False:
            BargainCartItem.objects.create(bargain = bargain, cart=cart)
            msg = u'Du har lagt till %s ' %bargain.title



    returnjson = {
            'cartitem': {
                'title': bargain.title
                },
            'message': { 'msg' : msg }
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

def voucher(request, pk):
	pk = pk.lower()
	if pk == 'vi-rabatt':
		key = _cart_id(request)
		cart, created = Cart.objects.get_or_create(key=key)
		voucher, created = VoucherCart.objects.get_or_create(cart = cart)
		voucher.save()
		print key
	else: 
		print 'fel kod'
		
	return redirect('/cart/show/')
	
def showcart(request):
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)
    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    voucher = cart.vouchercart_set.all()
    returntotal = totalsum(cartitems, bargains, request, voucher)
    getnames(cartitems)
    returntotal['cartitems'] =  cartitems
    returntotal['bargains'] =  bargains
    returntotal['voucher'] = voucher
  
    return render_to_response('cart/show_cart.html',
        returntotal,
        context_instance=RequestContext(request))


def editcartitem(request, key):

    try:
        cartitem = CartItem.objects.get(pk=key)
    except CartItem.DoesNotExist:
        cartitem = None

    listed = isincart(request, key, cartitem)

    if (listed == True):
        cartitem.color = Color.objects.get(order=cartitem.color)
        cartitem.pattern = Pattern.objects.get(order=cartitem.pattern)
        cartitem.size = Size.objects.get(id=cartitem.size)
        if cartitem.color_2 != 0:
            cartitem.color_2 = Color.objects.get(order=cartitem.color_2)
            cartitem.pattern_2 = Pattern.objects.get(order=cartitem.pattern_2)

        colors = Color.objects.filter(active=True, quality = cartitem.article.quality)
        patterns = Pattern.objects.filter(active=True, quality = cartitem.article.quality)
        sizes = Size.objects.filter(quality=cartitem.article.quality)


        return render_to_response('cart/detail.html',
            {'cartitem': cartitem,
             'colors': colors,
             'patterns': patterns,
             'sizes': sizes,
             },
            context_instance=RequestContext(request))
    else:
        return redirect('/cart/show/')

def removefromcart(request, pk, type):
    try:
        if type == 'bargain':
            cartitem = BargainCartItem.objects.get(pk=pk)
            
        else:
            cartitem = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        cartitem = None

    cartitem.delete()
    listed = isincart(request, pk, cartitem)

    if (listed == True):
        key = _cart_id(request)
        cart = Cart.objects.get(key=key)
        cartitems = cart.cartitem_set.all()
        bargains = cart.bargaincartitem_set.all()
        total = totalsum(cartitems, bargains)
        return_data = json.dumps(total)
        response = HttpResponse(return_data, mimetype="application/json")
        return response
    else:
        return redirect('/cart/show/')

def isincart(request, key, cartitem):
    key = _cart_id(request)
    cart = Cart.objects.get(key=key)
    cartitems = cart.cartitem_set.all()
    listed = False
    for item in cartitems:
        if (str(item) == str(cartitem)):
            listed = True

    if(listed):
        return True
    else:
        return False

def totalsum(cartitems, bargains, request, voucher):
    temp_p = 0
    temp_q = 0
    
    if (voucher and cartitems):
		try:
			ordered = sorted(cartitems, key=operator.attrgetter('article.price'), reverse=True) 
			print ordered
			ordered[0].article.oldprice = int(ordered[0].article.price)
			ordered[0].article.price = int(ordered[0].article.price * 0.85)
		except:
			pass 
				
    if (cartitems):			
        for item in cartitems:
            if item.article.discount:
                discount_price = f_discount(item.article)
                temp_p = temp_p + discount_price * item.quantity
                item.totalitemprice = discount_price * item.quantity
            else:
                temp_p = temp_p + item.article.price * item.quantity
                item.totalitemprice = item.article.price * item.quantity

            temp_q = temp_q + item.quantity

    if (bargains):
        for item in bargains:
            temp_p = temp_p + item.bargain.price
            temp_q = temp_q + 1
    try:
        gi = pygeoip.GeoIP(ROOT_DIR+'/GeoIP.dat')
        ip_ = request.META['REMOTE_ADDR']
        country = gi.country_code_by_addr(ip_)
    except:
        country = 'SE'

    if (country == 'SE'):
        se = True
        handling = 80

        if (temp_q > 3):
            handling = 120
        
        if (temp_p > 3000 or temp_p < 11):
            handling = 0

        temp_p = temp_p + handling

    else:
        se = False
        if (temp_q > 3):
            handling = 200
        else:
            handling = 100
        temp_p = temp_p + handling


    total = {'totalprice': temp_p, 'totalitems': temp_q, 'handling': handling, 'se': se}
    return total

def getnames(cartitems):
    for item in cartitems:
        item.color = Color.objects.get(order=item.color)
        item.pattern = Pattern.objects.get(order=item.pattern)
        item.size = Size.objects.get(id=item.size)
        if item.color_2:
            item.color_2 = Color.objects.get(order=item.color_2)
            item.pattern_2 = Pattern.objects.get(order=item.pattern_2)


def f_discount(item_article):
    item = item_article
    if (item.discount.type == 'P'):
        price_discount = (item.price * (100-item.discount.discount)) / 100
    else:
        price_discount = item.price - item.discount.discount

    return price_discount
