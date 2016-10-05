from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Cart, CartItem, BargainCartItem, VoucherCart, ReaCartItem
from django.http import HttpResponse
from products.models import Article, Color, Pattern, Size, Quality, Bargainbox, ReaArticle
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
from fortnox.fortnox import get_headers, searchCustomer, stockvalue_down
from django.contrib.auth.decorators import login_required
from logger.views import keepLog

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
        msg = ''
        sku = d['article_sku']
        article_db = Article.objects.get(sku_number = sku)
 
 
        try: 
            color = d['color']
            pattern = d['pattern']
            color2 = d['color2']
        except: 
            color = 0
            pattern = 0
            color2 = 0

        # if color2 exist then it is reversable zip jacket 
        if(color2 == 0):
            pass
        else:
            color2 = d['color2']
            pattern2 = d['pattern2']

        try: 
            size = d['size']
        except: 
            size = 1
        
        #  if article is metervara else te quatity is 1
        if sku == '3' or sku == '1000': 
            quantity = d['quantity'] 
        else: 
            quantity = 1

        cartitem_id = 1
        print "cart id", cartitem_id
        add_or_edit = d['add_or_edit']
        print "add or edit", add_or_edit

        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(key = cart_id)
        cart.save()

        existing_cartitems = CartItem.objects.filter(cart=cart)

        update = False

        # if costumer edits cart
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

        # if costumer adds a full varation 
        elif (cartitem_id and add_or_edit == 'full'):
            cartitem = CartItem.objects.create(cart = cart)
            cartitem.article = article_db
            cartitem.pattern = pattern
            cartitem.size = size
            cartitem.color = color
            cartitem.quantity = quantity
            if(color2 > 0):
                cartitem.color_2 = color2
                cartitem.pattern_2 = pattern2
            cartitem.save()
            msg = u'Du har lagt till: <br/>'

        # if costumer adds a varation 

        elif (cartitem_id and add_or_edit == 'add'):
            print "ist add"
            cartitem = CartItem.objects.create(cart = cart)
            cartitem.article = article_db
            cartitem.pattern = pattern
            cartitem.size = size
            cartitem.color = color
            cartitem.quantity = quantity
            if(color2 > 0):
                cartitem.color_2 = color2
                cartitem.pattern_2 = pattern2
            cartitem.save()
            msg = u'Du har lagt till: <br/>'
        else: 
            print "o no"
            pass

        # if there is cart item in the shopping cart check if it is the same.     
        if (existing_cartitems):
            for item in existing_cartitems:
                if (str(item.article.sku_number) == str(sku) and str(item.pattern) == str(pattern) and
                    str(item.color) == str(color) and str(item.size) == str(size)):
                    item.quantity = quantity
                    item.save()
                    msg = u'Antal 1,  %s <br/>' %(article_db.name)
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
                msg = u'Du har lagt till: <br/>'                   
                cartitem.save()
        try: 
            color_db = Color.objects.get(order=color)
            pattern_db = Pattern.objects.get(order=pattern)
        except:
            color_db = Color.objects.get(order=1)
            pattern_db = Pattern.objects.get(order=1)

        try: 
            size_db = Size.objects.get(pk=size)
            size_db = size_db.name
        except:
            size_db = getsize(int(size))

        if(color2 == '0'):
            pass
        else:
            color_db2 = Color.objects.get(order = color2)
            pattern_db2 = Pattern.objects.get(order = pattern2)

        if(color2 != '0'):
            returnjson = {
                    'cartitem': {
                        'article': article_db.name,
                        'sku' : sku,
                        'color': color_db.name,
                        'pattern': pattern_db.name,
                        'color2': color_db2.name,
                        'pattern2': pattern_db2.name,
                        'size': size_db,
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
                        'size': size_db,
                        'quantity': quantity,
                        },
                    'message': { 'msg' : msg  }
                }

        return_data = json.dumps(returnjson)
        log = 'Cart add: ' + article_db.name + ' ' + sku  + ' ' + color_db.name + ' ' + pattern_db.name + ' ' + size_db
        keepLog(request, log, 'INFO', '', cart_id) 

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

def add_rea(request):
    if request.POST:
        d = request.POST
        item = d['item']
        print item
        rea = ReaArticle.objects.get(pk=item)

        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(key = cart_id)
        cart.save()

        existing_reaitems = ReaCartItem.objects.filter(cart=cart)
       
        inbox = False

        for  existing_reaitems in existing_reaitems:
            if rea.pk == existing_reaitems.reaArticle.pk:
                msg = u'Fyndet finns redan '
                 
                inbox = True

        if inbox == False:
            ReaCartItem.objects.create(reaArticle=rea, cart=cart)
            msg = u'Du har lagt till %s ' %rea.article.name



    returnjson = {
            'cartitem': {
                'title': rea.article.name
                },
            'message': { 'msg' : msg }
        }

    log = 'Rea add: ' + rea.article.name
    keepLog(request, log, 'INFO', '', cart_id) 

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
    cart_id = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=cart_id)
    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    rea = cart.reacartitem_set.all()
    voucher = cart.vouchercart_set.all()
    returntotal = totalsum(cartitems, bargains, request, voucher, rea)
    getnames(cartitems)
    returntotal['cartitems'] =  cartitems
    returntotal['bargains'] =  bargains
    returntotal['voucher'] = voucher
    returntotal['rea'] = rea

    return render_to_response('cart/show_cart.html',
        returntotal,
        context_instance=RequestContext(request))

def showcartBySessionId(request, session_id):
    if request.user.is_authenticated:
        key = session_id
        try:
            cart = Cart.objects.get(key=key)
            cartitems = cart.cartitem_set.all()
            bargains = cart.bargaincartitem_set.all()
            rea = cart.reacartitem_set.all()
            voucher = cart.vouchercart_set.all()
            returntotal = totalsum(cartitems, bargains, request, voucher, rea)
            getnames(cartitems)
            returntotal['cartitems'] =  cartitems
            returntotal['bargains'] =  bargains
            returntotal['voucher'] = voucher
            returntotal['rea'] = rea
        except:
            returntotal = ''

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
        elif type == 'rea': 
            cartitem = ReaCartItem.objects.get(pk=pk)
        else:
            cartitem = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        cartitem = None

    try:
        log = 'Cartitem remove: ' + cartitem.article.name 
        keepLog(request, log, 'INFO', '', pk) 
    except:
        log = 'Cartitem remove failed' 
        keepLog(request, log, 'ERROR', '', pk) 

    cartitem.delete()
    listed = isincart(request, pk, cartitem)

    if (listed == True):
        key = _cart_id(request)
        cart = Cart.objects.get(key=key)
        cartitems = cart.cartitem_set.all()
        bargains = cart.bargaincartitem_set.all()
        rea = []
        voucher = []
        total = totalsum(cartitems, bargains, request, voucher, rea)
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

def totalsum(cartitems, bargains, request, voucher, rea):
    temp_p = 0
    temp_q = 0
    
    if (voucher and cartitems):
		try:
			ordered = sorted(cartitems, key=operator.attrgetter('article.price'), reverse=True)
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

    if (rea):
        for item in rea:
            temp_p = temp_p + item.reaArticle.rea_price
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

def getsize(size):
    temp_size = size

    if size == 34 or size == 1: 
        return_size = 'XS' 
    elif size == 36 or size == 2: 
        return_size = 'S'
    elif size == 3840 or size == 3: 
        return_size = 'M'
    elif size == 42 or size == 5: 
        return_size = 'L'
    elif size == 44 or size == 6: 
        return_size = 'XL'  
    elif size == 46 or size == 7:
        return_size = 'XLL'
    else: 
        return_size = 'NO'

    if return_size == 'NO':
        print "noooooooooo"
        try: 
            size_db = Size.objects.get(pk=size)
            size_db = size_db.name
        except: 
            pass 

    return return_size

def getnames(cartitems):
    for item in cartitems:
        item.color = Color.objects.get(order=item.color)
        item.pattern = Pattern.objects.get(order=item.pattern)
        try: 
            item.size = Size.objects.get(pk=item.size)
        except:
            item.size = getsize(item.size)
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



# I want to handel customer here
@login_required
def customer_email(request, email):

    if request.user.is_superuser:    
        name = ''
        headers = get_headers()
        customer = searchCustomer(headers, name, email) 
    else:
        customer = 'you not admin'


    return render_to_response('cart/admin_customer.html', {
        'customer': customer, 
    }, context_instance=RequestContext(request))



