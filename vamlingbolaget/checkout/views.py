#-*-coding:utf-8-*-

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core import mail
from cart.views import _cart_id, totalsum, _new_cart_id, getnames
from products.models import *
from cart.models import Cart, CartItem
from orders.models import OrderItem, ReaOrderItem
from forms import CheckoutForm
from models import Checkout
import random
from payex.service import PayEx
from fortnox.fortnox import get_headers, get_art_temp, json_update, update_article, CreateCostumer, searchCustomer, customerExistOrCreate, updateCostumer, seekOrder, createOrder, createNewOrder, create_invoice_rows, getOrders, seekOrderByNumber, formatJson, create_order_rows, getFortnoxSize
import json
import time
import datetime
from translator import toEnglish
from klarna import get_order, confirm_order, klarna_cart, get_data_defaults, get_testcart, confirm_order_with_klarna
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import ObjectDoesNotExist
from make_messages import head_part_of_message, adress_part_of_message, cart_part_of_message, cartsum_part_of_message, final_part_of_message, personal_part_of_message, email_one
from logger.views import keepLog

# --> from /checkout/ pay --> with card | on delivery
def checkout(request, test=''):
    if test  == 'test':
        print 'katten'
    url_klarna = request.path
    template_url = 'checkout/checkout_b.html'
    # get the all cart data
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)


    try:
        bargains = cart.bargaincartitem_set.all()
        print(bargains)
    except:
        pass

    try:
        rea_items = cart.reacartitem_set.all()
    except:
        pass

    try:
        cartitems = cart.cartitem_set.all()
    except:
        pass

    try:
        test_ip = request.META['REMOTE_ADDR']
        if (test_ip == '90.230.236.251'):
            print test_ip
            template_url = 'checkout/checkout_b.html'
    except:
        pass

    voucher = cart.vouchercart_set.all()
    getnames(cartitems)

    # get price details
    returntotal = totalsum(cartitems, bargains, request, voucher, rea_items)
    totalprice = returntotal['totalprice']
    totalitems = returntotal['totalitems']
    handling = returntotal['handling']
    sweden = returntotal['se']

    # handel the form
    form = CheckoutForm()
    returntotal['form'] = form

    try:
        lang = request.LANGUAGE_CODE
    except:
        lang = 'sv'

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():
            # start the order process and store form values
            new_order = form.save(commit=False)

            # create a new order number

            epoch = int(time.time())
            order_num = (epoch -1400000000)
            new_order.order_number = order_num
            new_order.order_number = get_ordernumber()

            new_order.ip = request.META['REMOTE_ADDR']

            sms = request.POST['sms']

            zip = request.POST['postcode']
            try:
                zip = zip.replace(" ", "")
                zip = int(zip)
            except:
                log = 'Error zip code'
                keepLog(request, log, 'ERROR', new_order.ip, zip)
                zip = 11122

            new_order.postcode = zip
            new_order.status = 'O'
            new_order.paymentmethod = request.POST['paymentmethod']
            new_order.order = ''
            if (sms == 'yes'):
                new_order.post = True
            else:
                new_order.post = False

            # start creating the costumer message
            #temp_msg = head_part_of_message(lang)
            #temp_msg = temp_msg + cart_part_of_message(cartitems, rea_items, lang)
            #temp_msg = temp_msg + cartsum_part_of_message(handling, totalprice, lang)


            #mess = request.POST['message']
            #if len(mess) > 2:
                #temp_msg = temp_msg + personal_part_of_message(mess, lang)

            #save the message at this stage to continue on for klarna
            #new_order.message = temp_msg


            # get the session_key for look up
            new_order.session_key = _cart_id(request)

            try:
                new_order.save()
            except:
                epoch = int(time.time())
                order_num = (epoch -1400000000)
                new_order.order_number = order_num
                new_order.save()

            # make an email body

            # add adress part of message
            #temp_msg = temp_msg + adress_part_of_message(new_order, lang)

            #finalize the message including ordernumber and session key
            #the_message = temp_msg + final_part_of_message(new_order, lang)
            the_items = getCartItems(request)
            cartitems = the_items['cartitems']
            returntotal = totalsum(cartitems, bargains, request, voucher, rea_items)
            reaitems = the_items['rea_items']

            CheckoutTransfer(new_order, cartitems, reaitems)
            log = 'Checkout Transfer Success'
            keepLog(request, log, 'INFO', new_order.ip, key)

            try:
                for item in cartitems:
                    if (item.article.discount.discount > 0):
                        new_order.payment_log = item.article.discount.discount
            except:
                pass
            email_body = email_one(request, new_order, cartitems, bargains, reaitems, handling, totalprice)
            new_order.message = email_body
            new_order.save()


            # payment logic start

            # if costumer pay on delivery
            # we just send and email with order to vamlingbolaget and a copy to the coustumer and redirect to the thanks url
            # we also save the order in json that we can use with fortnox, as well as staring the payment log
            if (new_order.paymentmethod == 'P'):

                #new_order.message = the_message

                # start payment log
                log = 'New Order - Pay on Delivery, ' + request.POST['email']
                keepLog(request, log, 'INFO', new_order.ip, key)
                log = 'Sending Mail order to ' + request.POST['email']
                keepLog(request, log, 'INFO', new_order.ip, key)

                # save the order again
                new_order.save()

                # send email verifaction to customer if name not Tester
                to = [request.POST['email'], 'info@vamlingbolaget.com']
                if (new_order.first_name == "Tester"):
                    mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %email_body, 'palle.torsson@gmail.com', to,  fail_silently=False)
                else:
                    mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %email_body, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)

                return HttpResponseRedirect('thanks/')

            # If costumer use Klarna
            if (new_order.paymentmethod == 'K'):

                #prevent database duplication
                try:
                    new_order = Checkout.objects.get(session_key=new_order.session_key)

                except:
                    new_order.save()

                # start klarna payment log
                log = 'Initialize Klarna Checkout, ' + request.POST['email']
                keepLog(request, log, 'INFO', new_order.ip, key)
                # save the order

                new_order.save()

                # make cart for klarna
                # new_order.order = json.dumps(order_json)
                klarna_cart_obj = getCartItems(request)
                klarna_cart_obj = klarna_cart(klarna_cart_obj)

                # create html the return
                klarna_order  = get_data_defaults(klarna_cart_obj)
                klarna_obj = get_order(klarna_order)
                klarna_html = klarna_obj['html']

                # create and save klarna key
                new_order.payex_key = klarna_obj['order_id']
                new_order.save()

                # TODO concider this block the order is not saved...
                if not request.session.exists(request.session.session_key):
                    request.session.create()

                request.session["klarna_id"] = klarna_obj['order_id']

                return render_to_response('checkout/klarna.html', {
                    'klarna': klarna_html,
                    'k_session': request.session["klarna_id"]
                }, context_instance=RequestContext(request))


            # if costumer pay with card we need to start a PayEx service
            if (new_order.paymentmethod == 'C'):

                # Initialize PayEx service
                service = PayEx(
                    merchant_number=settings.PAYEX_MERCHANT_NUMBER,
                    encryption_key=settings.PAYEX_ENCRYPTION_KEY,
                    production=settings.PAYEX_IN_PRODUCTION
                    )

                price = totalprice * 100
                payex_products = 'Vamlingbolaget'
                payex_articles = 'Vamlingbolaget'
                response = service.initialize(
                    purchaseOperation='SALE',
                    price=price,
                    currency='SEK',
                    vat='2500',
                    orderID=new_order.order_number,
                    productNumber=payex_products,
                    description=payex_articles,
                    clientIPAddress=new_order.ip,
                    clientIdentifier='USERAGENT=test&username=testuser',
                    additionalValues='',
                    returnUrl='http://www.vamlingbolaget.com/checkout/success',
                    view='CREDITCARD',
                    cancelUrl='http://www.vamlingbolaget.com/checkout/cancel'
                )

                try:
                    PayExRefKey = response['orderRef']
                except:
                    PayExRefKey = 1

                new_order.payex_key = PayExRefKey
                #new_order.message = the_message
                # log
                log = 'Initialize PayEx Process, ' + request.POST['email']
                keepLog(request, log, 'INFO', new_order.ip, key)
                new_order.order = ''
                # save the order
                new_order.save()
                return HttpResponseRedirect(response['redirectUrl'])

    if url_klarna == "/checkout/klarna/":
        klarna_test = '1'
    else:
        klarna_test = '0'

    return render_to_response(template_url, {
        'form': form,
        'totalprice': totalprice,
        'totalitems': totalitems,
        'handling': handling,
        'cartitems': cartitems,
        'bargains' : bargains,
        'rea' : rea_items,
        'sweden': sweden,
        'voucher': voucher,
        'klarna_test': klarna_test,
        'showtopmenu': True
        },
        context_instance=RequestContext(request))

def success(request):
    # if payex Transaction was successfully performed we finalize the order

    service = PayEx(
        merchant_number=settings.PAYEX_MERCHANT_NUMBER,
        encryption_key=settings.PAYEX_ENCRYPTION_KEY,
        production=settings.PAYEX_IN_PRODUCTION
    )

    # try to get ip else set ip to None
    try:
        ip = request.META['REMOTE_ADDR']
    except:
        ip = 'None'

    # orderRef is the the payex_key if its not found log error to console (this is very unlikly)
    try:
        orderref = request.GET.get('orderRef', None)
    except:
        log = 'No orderRef found'
        keepLog(request, log, 'ERROR', ip)

    if orderref:
        response = service.complete(orderRef=orderref)

		# if we get a good responce from sevice complite
        if (response['status']['errorCode'] == 'OK' and response['transactionStatus'] == '0'):

            # get cart id from request
            cart_id = _cart_id(request)

            # get the checkout
            try:
                order = Checkout.objects.get(payex_key=orderref)
                log = u'Log Success: Checkout found with the payex_key: ' +  orderref + ' Cartid: ' + cart_id
                keepLog(request, log, 'INFO', ip, cart_id)
            except:
                order = 1
                log = 'Log Error: no checkout found with the payex_key: ' + str(orderref)
                keepLog(request, log, 'ERROR', ip, cart_id)

            # in the unlily event that the checkout can't be found send a coustmer to thanks url with a message to contact vamlingbolaget.
            if (order == 1):
                message = u'Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com.'
                return render_to_response('checkout/thanks.html', {
                    'message': message,
                }, context_instance=RequestContext(request))

            # remove the old cart and cart items if status is Order
            if (order != 1 and order.status == 'O'):

                try:
                    order_obj = formatJson(order.order)
                    order_obj = json.loads(order_obj)
                    order.order = order_obj
                    order.save()
                except:
                    pass

                try:
                    transnumber = response['transactionNumber']
                    order.shipping_country = transnumber
                    order.message = order.message + 'PayEx transaktion: ' + str(transnumber)
                    order.status = 'P'
                    order.save()
                    # logging
                    log = 'Log Success: PayEx transaktion: ' + str(transnumber) + '\n'
                    keepLog(request, log, 'INFO', ip, cart_id)
                except:
                    log = 'Log Success Fail, PayEx transaktion not found: ' + str(transnumber)
                    keepLog(request, log, 'ERROR', ip, cart_id)

                try:
                    to = [order.email, 'info@vamlingbolaget.com']
                    mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %order.message, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)
                    order.message = order.message + u'Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com.'
                    # logging
                    log = u'4: Log Success: Mail sent to mail adress : ' + order.email
                    keepLog(request, log, 'INFO', ip, cart_id)
                except:
                    log = u'4: Log Fail: Mail not sent to mail adress : ' + str(order.email)
                    keepLog(request, log, 'ERROR', ip, cart_id)


                message = "Tack for din order"

                return render_to_response('checkout/thanks.html', {
                    'order': order,
                    'message': message
                }, context_instance=RequestContext(request))

            else:
                message = u"Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com."
                return render_to_response('checkout/thanks.html', {
                    'message': message
                }, context_instance=RequestContext(request))


        else:
            try:
                order = Checkout.objects.get(payex_key=orderref)
            except:
                order = 1

            if(order == 1):
                message = u"- Det finns inte någon sådan beställning"

                # logging
                log = u'2: Cancel log: - det fanns ingen beställning att avbryta'
                keepLog(request, log, 'ERROR', ip)

                return render_to_response('checkout/thanks.html', {
                'message': message,
                }, context_instance=RequestContext(request))

            else:
                order.status = 'C'
                order.save()
                message = u"- Betalningen avslogs eller avbröts."

                # logging
                log = u'2: Cancel log: - Betalningen avslogs eller avbröts.'
                keepLog(request, log, 'ERROR', ip)

            return render_to_response('checkout/thanks.html', {
                'message': message,
                'cancel':1,
            }, context_instance=RequestContext(request))
    else:
        message = "Skicka en order eller utforska utbudet"
        return render_to_response('checkout/thanks.html', {
            'message': message
        }, context_instance=RequestContext(request))



# create a unique order number by recursive funtion
def get_ordernumber():
    rand = random.randrange(0, 111111, 3)
    try:
        order = Checkout.objects.get(order_number=rand)
        order_exist = 1
    except:
        order_exist = 0

    if (order_exist == 1):
        rand = get_ordernumber()
    else:
        return rand


# if payment canceled
def cancel(request):
    try:
        ip = request.META['REMOTE_ADDR']
    except:
        ip = None
    cart_id = _cart_id(request)
    try:
        order = Checkout.objects.get(session_key=cart_id)
    except:
        order = 0

    if(order == 0):
        pass
    else:
        log = 'Payment canceled'
        keepLog(request, log, 'ERROR', ip, cart_id)

    return HttpResponseRedirect('/checkout/')

def thanks(request):
    try:
        ip = request.META['REMOTE_ADDR']
    except:
        ip = None

    cart_id = _cart_id(request)

    try:
        checkout = Checkout.objects.filter(session_key=cart_id)[0]
    except:
        checkout = 1
        log =  "Thanks url hit but no checkout found"
        keepLog(request, log, 'WARN', ip, cart_id)
        return HttpResponseRedirect('/')

    if (checkout != 1):
        try:
            log = "Displaying thanks you message"
            keepLog(request, log, 'INFO', ip, cart_id)
        except:
            log =  "Log Thanks: can not find order"
            keepLog(request, log, 'INFO', ip, cart_id)

        message = "Tack for din order"

    else:
        message = u"Lägg till något i din shoppinglåda och gör en beställning."

    # TODO internationalize these messages
    klarna_html_res = '<div class="text-center"><hr><button type="button" class="btn btn-large btn-success text-center"> Tack för ditt köp! </button><hr></div>'
    return render_to_response('checkout/thanks.html', {
        'order': checkout,
        'message': message,
        'klarna_html': klarna_html_res,
    }, context_instance=RequestContext(request))

def klarna_push(request, klarna_id):

    try:
        checkout = Checkout.objects.filter(payex_key=klarna_id)[0]
        print checkout
        checkout.status = 'F'
        checkout.save()
    except:
        confirm_ok = 'no such checkout'
        return HttpResponse(confirm_ok)

    confirm_ok = confirm_order_with_klarna(klarna_id)

    return HttpResponse(confirm_ok)


def klarna_thanks(request):
    try:
        log_ip = request.META['REMOTE_ADDR']
    except:
        log_ip = 'none'

    cart_id = _cart_id(request)
    #klarna_html = 'none'

    try:
        checkout = Checkout.objects.filter(session_key=cart_id)[0]
    except:
        checkout = 0
        log =  "Klarna thanks url hit but no checkout found"
        keepLog(request, log, 'WARN', log_ip, cart_id)
        return HttpResponseRedirect('/')

    message = "Tack for din order"

    klarna_html = confirm_order(checkout.payex_key)
    klarna_html_res = klarna_html["html"]

    adress = klarna_html['billingadress']
    #checkout.order = klarna_html['shipping_address']
    checkout.first_name = adress['family_name']
    checkout.last_name = adress['given_name']
    checkout.email = adress[ 'email']
    checkout.phone = adress['phone']
    checkout.postcodee = adress['postal_code']
    checkout.street = adress['street_address']
    checkout.country = adress['country']
    checkout.save()

    # add adress part of message
    lang = request.LANGUAGE_CODE
    temp_msg = checkout.message
    temp_msg = temp_msg + adress_part_of_message(checkout, lang)


    #finalize the message including ordernumber and session key
    the_message = temp_msg + final_part_of_message(checkout, lang)

    # save message
    checkout.message = the_message
    checkout.save()

    if (checkout != 0):
        try:
            log = 'Sending mail order conformation to: ' + checkout.email
            keepLog(request, log, 'INFO', checkout.ip, cart_id)
        except:
            pass

    the_items = getCartItems(request)
    cartitems = the_items['cartitems']
    reaitems = the_items['rea_items']

    CheckoutTransfer(checkout, cartitems, reaitems)

    return render_to_response('checkout/thanks.html', {
        'order': checkout,
        'message': message,
        'klarna_html': klarna_html_res,
    }, context_instance=RequestContext(request))


def payexCallback(request):
    # transactionRef =<String(32)>&transactionNumber=<Integer(7-9)>&orderRef=<String(32)>
    # also check the ip

    # try to get ip else set ip to None
    try:
        ip = request.META['REMOTE_ADDR']
    except:
        ip = 'None'

    raw_request = request

    try:
        transactionRef = request.GET['transactionRef']
    except:
        transactionRef = 'None'

    try:
        transactionNumber = request.GET['transactionNumber']
    except:
        transactionNumber = 0

    try:
        orderRef = request.GET['orderRef']
    except:
        orderRef = 'None'

    try:
        order = Checkout.objects.get(payex_key=orderRef)
    except:
        order = 1

    if (order != 1):
        log =   '4; Payex callback Log: PayEx transaktionNumber, transactionRef: ' + str(transactionNumber) + ', ' + str(transactionRef) + ' orderRef: ' + str(orderRef) + ', from ip: '+ ip + '\n'
        keepLog(request, log, 'INFO', ip, str(transactionNumber))

    return HttpResponse(status=200)



def fortnox(request):
    log = ''
    cart_id = _cart_id(request)
    try:
        ip = request.META['REMOTE_ADDR']
    except:
        ip = 'None'

    try:
        order_id = request.POST['order_id']
    except:
        order_id = 0
    # get order from databas
    if (order_id != 0):
        try:
            order = Checkout.objects.get(order_number=order_id)
        except:
            order = Checkout.objects.filter(order_number=order_id)
            order = order.reverse()[0]
            log = 'Duplicate order nummer'
            keepLog(request, log, 'WARN', ip)

        # - all item in the cat
        try:
            the_items = getCartItems(request)
        except:
            log = 'Error, cartitems'
            keepLog(request, log, 'ERROR', ip)

        # set the fortnox input to order and not invoice
        what = "invoice"

        # create the json base for the fortnox order and save to database
        try:
            json_order = the_items
            final_orderjson = fortnoxOrderandCostumer(request, order, json_order, what)
            order.order = final_orderjson
            order.save()
            log = log + ' Creating order_json bacis for order: ' + str(order_id)
            order_ok_json = True
        except:
            log = log + ' Fortnox Error when adding Fortnox order'
            order_ok_json = False



        # set the new stock
        try:
            cleanCartandSetStock(request, the_items)

            log = log + ' Cleaning cart'
            keepLog(request, log, 'INFO', ip)
        except:
            log = log + ' Error cleaning cart'
            keepLog(request, log, 'ERROR', ip)

        return HttpResponse(status=200)
    else:
        return HttpResponseRedirect('/')

# clean cart and chang stockquanity
def cleanCartandSetStock(request, the_items):
     # create a clean new cart
    _new_cart_id(request)

    # get cart, key and items

    # update rea stock in django databse
    cartitems = the_items['cartitems']
    print cartitems
    bargains = the_items['bargains']
    voucher = the_items['voucher']
    rea_items = the_items['rea_items']

    try:
        for item in rea_items:
            current_stock = item.reaArticle.stockquantity
            new_stock = current_stock - 1
            item.reaArticle.stockquantity = new_stock

            if (current_stock == 1):
                item.reaArticle.status = 'E'
            item.reaArticle.save()
    except:
        print "clean wrong"

    for item in cartitems:
        print "-", item
        try:
            article = Article.objects.get(sku_number=item.article.sku_number)
            pattern = Pattern.objects.get(order=item.pattern)
            color = Color.objects.get(order=item.color)
            variation = Variation.objects.get(article=article, pattern=pattern, color=color)
            print "--", variation
            print "--", item.size
            full_var = FullVariation.objects.get(variation=variation, size=item.size)
            print "--", full_var
            current_stock = full_var.stock
            print "----", current_stock
            if current_stock > 0:
                new_stock = current_stock - 1
                full_var.stock = new_stock
                full_var.save()
                log = 'New stock'
                try:
                    print "-----", new_stock
                    old_new_stock = "old: " + str(current_stock) + " new: " + str(new_stock) + " art: " + str(full_var)
                    keepLog(request, log, 'INFO', '', old_new_stock)
                except:
                    pass
        except:
            pass

    # remove all caritem from that cart and the cart
    try:
        rea_items.delete()
    except:
        pass

    try:
        cartitems.delete()
    except:
        pass

    try:
        bargains.delete()
        voucher.delete()
    except:
        pass

    try:
        cart.delete()
    except:
        pass


    return 1

def getCartItems(request):

    key = _cart_id(request)
    cart = Cart.objects.get(key = key)
    cartitems_key = cart.id

    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    voucher = cart.vouchercart_set.all()
    try:
        rea_items = cart.reacartitem_set.all()
        #ret = append(rea_items)
    except:
        print "clean wrong"

    allitems = {'cartitems': cartitems, 'bargains': bargains, 'voucher': voucher, 'rea_items': rea_items}

    return allitems

def getCustumer(new_order):

    fullname = unicode(new_order.first_name) + " " + unicode(new_order.last_name)

    return json.dumps({
            "Customer": {
                "Name": unicode(fullname),
                "Address1": unicode(new_order.street),
                "City": unicode(new_order.city),
                "ZipCode": new_order.postcode,
                "Email": unicode(new_order.email),
                "Phone1": new_order.phone,
                "SalesAccount": "3012",
            }
        })

# Run after order when customer is send to conferm url /thanks/
def fortnoxOrderandCostumer(request, new_order, order_json, what):
    customer_no = '0'
    customer = getCustumer(new_order)
    headers = get_headers()

    # To make an Fortnox order we need a Custumer
    # first check if customer exist
    # and update or create customer and get customer number back and log
    try:
        customer_no = customerExistOrCreate(headers, customer, order_json)
    except:
        log = 'Fortnox customer not resolved'
        keepLog(request, log, 'ERROR', '', customer)

    # Creat the order part of the json from order_json and log --> fortnox.py
    if what == 'invoice':
        try:
            invoice_rows = create_invoice_rows(order_json)
        except:
            pass
    # order_json is a string
    elif what == 'order_json_done':
        invoice_rows = order_json

        try:
            invoice_rows = formatJson(order_json)
            invoice_rows = json.loads(invoice_rows)
        except:
            pass

        log = 'order this done json, its invoices...'
        keepLog(request, log, 'INFO', customer, '', invoice_rows)
    else:
        try:
            order_rows = create_order_rows(order_json)
            log = 'Fortnox order json...'
            keepLog(request, log, 'INFO', customer, '', order_json)
        except:
            log = 'Fortnox order json not resolved'
            keepLog(request, log, 'ERROR', customer, '', order_json)
            invoice_rows = new_order.order

    # add additional information to comment and invoice type feilds

    # set invoice typ
    invoice_type = new_order.paymentmethod
    if(invoice_type == 'P'):
        invoice_type_value = 'INVOICE'
    else:
        invoice_type_value = 'CASHINVOICE'

    # try to add a comments and add it to as a description row in fortnox

    try:
        orderid_ = new_order.order_number
        comments = "OrderNr:" + unicode(orderid_)
    except:
        comments = ""

    # I use shipping_country to store the payex transkey
    try:
        if int(new_order.shipping_country) > 1:
            comments = comments + " - PayexNr:"  + unicode(new_order.shipping_country)
    except:
        pass

    try:
        invoice_rows["Invoice"]["InvoiceRows"].append({
                "Description": unicode(comments)
            })
    except:
        pass

    try:
        invoice_rows = invoice_rows["Invoice"]["InvoiceRows"]
    except:
        invoice_rows = invoice_rows

    if (what == 'order_json_done'):
        all_rows = json.dumps({
                "Invoice": {
                    "InvoiceRows": invoice_rows,
                    "CustomerNumber": customer_no,
                    "Comments": comments,
                    "YourOrderNumber": orderid_,
                    "InvoiceType": invoice_type_value,
                }
            })

    if what == 'invoice':
        customer_order = json.dumps({
                    "Invoice": {
                        "InvoiceRows": invoice_rows,
                        "CustomerNumber": customer_no,
                        "Comments": comments,
                        "YourOrderNumber": orderid_,
                        "InvoiceType": invoice_type_value,
                    }
                })

    elif what == 'order_json_done':
        customer_order = all_rows
    else:
        customer_order = json.dumps(
            {
                "Order":
                {
                "CustomerNumber": customer_no,
                "OrderRows": order_rows
                }
            })

    return customer_order

# to show all checkouts
def admin_view(request, limit):
    orders = Checkout.objects.all()
    the_art = False
    numbers = []
    res = []

    for order in orders:
        order.art = "----"
        # ta fram artikelnummet
        try:
            start = order.order.index(' st ') + len(' st ')
            end = order.order.index( ') i ', start )
            if (len(order.order[start:end]) < 120):
                order.art = order.order[start:end]
                order.art = order.art[-4:]
                print order.art, order.id
                the_art = True

        except:
            the_art = False
            pass

        if the_art == False:
            try:
                start = order.order.index('uct 1:') + len('uct 1:')
                end = order.order.index( ') i ', start )

                if (len(order.order[start:end]) < 120):
                    order.art = order.order[start:end]
                    print "-Pc!", order.art, order.id
                    the_art = True

            except:
                the_art = False
                pass

        if the_art == False:
            try:
                start = order.order.index('ArticleNumber":') + len('ArticleNumber":')
                end = order.order.index( ',', start )

                if (len(order.order[start:end]) < 120):
                    order.art = order.order[start:end]
                    order.art = order.art.replace("\"", "")
                    print "-Arti!-", order.art, order.id
                    the_art = True

            except:
                the_art = False
                pass

        if the_art == False:
            try:
                start = order.message.index('kel:') + len('kel:')
                end = order.message.index( ')', start )

                if (len(order.message[start:end]) < 120):
                    order.art = order.message[start:end]
                    print "-MessArti!-", order.art, order.id

                    start = 3
                    end = start + 4
                    order.art = order.art[-4:]
                    print "-MessArti! 2-", order.art
                    the_art = True

            except:
                the_art = False
                pass
        #print "----- end: ", the_art, order.id

        try:
            start = order.order.index(' st ') + len(' st ')
            end = order.order.index( ' (', start )
            if (len(order.order[start:end]) < 120):
                order.artname = order.order[start:end]
        except:
            pass
        # ta fram storlek
        try:
            start = order.order.index('Storlek: ') + len('Storlek: ')
            end = order.order.index( 'Pris', start )
            if (len(order.order[start:end]) < 120):
                order.size = order.order[start:end]
        except:
            pass
        try:
            start = order.order.index(' i ') + len(' i ')
            end = order.order.index( ', ', start )
            if (len(order.order[start:end]) < 120):
                order.pattern = order.order[start:end]
        except:
            pass

        try:
            start = order.order.index(', ') + len(', ')
            end = order.order.index( 'Storlek:', start )
            if (len(order.order[start:end]) < 120):
                order.color = order.order[start:end]
        except:
            pass

        order.order = order.order[86:]
        order.order = order.order[:100]
        if (the_art != False):
            numbers.append(order.art)
    set_art = set()
    for n in numbers:
        set_art.add(n)

    #set_art = sorted(set_art)
    for art in set_art:
        i = {}
        i['art'] = art
        i['occ'] = str(numbers.count(art))
        res.append(i)


    return render_to_response('checkout/admin_view.html', {
        'orders': orders,
        'res': res

    }, context_instance=RequestContext(request))


# to show all checkouts
def rea_admin_views(request, limit):
    orders = Checkout.objects.all().order_by('-id')[:limit]

    for order in orders:
        rea = None
        try:
            start = order.message.index('Produkt 1: ') + len('Produkt 1: ')
            end = order.message.index( ' :', start )

            if (len(order.message[start:end]) < 120):
                rea = order.message[start:end]
        except:
            pass

        if (rea == 'rea'):
            try:
                start = order.message.index(' rea : ') + len(' rea : ')
                end = order.message.index( ' : ', start )
                if (len(order.message[start:end]) < 120):
                    order.art = order.message[start:end].rstrip('\n')
            except:
                pass

            try:
                start = order.message.index('Storlek') + len('Storlek')
                end = order.message.index( 'Frakt', start )
                if (len(order.message[start:end]) < 120):
                    order.size = order.message[start:end].rstrip('\n')

            except:
                pass

            try:
                start = order.message.index('i ') + len('i ')
                end = order.message.index( ', ', start )
                if (len(order.message[start:end]) < 120):
                    order.pattern = order.message[start:end].rstrip('\n')
            except:
                pass

            try:
                start = order.message.index(', ') + len(', ')
                end = order.message.index( 'Storlek', start )
                if (len(order.message[start:end]) < 120):
                    order.color = order.message[start:end].rstrip('\n')
            except:
                pass

        order.message = order.message[86:]
        order.message = order.message[:100]

    return render_to_response('checkout/rea_admin_view.html', {
        'orders': orders,
    }, context_instance=RequestContext(request))

def rea_admin_total(request, limit):
    orders = Checkout.objects.all().order_by('-id')[:limit]
    reaart = ReaArticle.objects.all()
    rtotal = 0
    l = len(orders)
    name = ''

    for art in reaart:
        p = art.rea_price
        rtotal = rtotal + p

    total = 0
    old_email = 'first'

    for order in orders:
        tempprice = 0
        email = order.email
        rea = None

        try:
            start = order.message.index('Produkt 1: ') + len('Produkt 1: ')
            end = order.message.index( ' :', start )

            if (len(order.message[start:end]) < 120):
                rea = order.message[start:end]
        except:
            pass

        if(email == old_email):
            rea = 'allready'
            tempprice = 0

        if(order.status == 'C'):
            rea = 'allready'
            tempprice = 0

        old_email = email

        if (rea == 'rea'):
            try:
                start = order.message.index('Totalpris: ') + len('Totalpris: ')
                end = order.message.index( ' SEK', start )
                if (len(order.message[start:end]) < 120):
                    tempprice = order.message[start:end].rstrip('\n')

            except:
                tempprice = 0

        total = total + int(tempprice)

        l = l - 1

        if (l < 2):
            name = order.first_name


    return render_to_response('checkout/rea_admin_total.html', {
        'total': total,
        'rtotal': rtotal,
        'name': name
    }, context_instance=RequestContext(request))


def pacsoft(request):
    message = "add adress"

    return render_to_response('checkout/pacsoft.html',
        message,
        context_instance=RequestContext(request))



def testingRemoveStock(request):
    #message = cleanCartandSetStock(request)
    message = 'session test'
    request.session['test'] = 'test'
    request.session['has_commented'] = True
    return render_to_response('checkout/tests.html', {
        'message': message,
        'session_': request.session


    }, context_instance=RequestContext(request))


def consumOrder(request, order_id, force):
    if request.user.is_authenticated():
        try:
            order = Checkout.objects.filter(order_number=order_id).order_by('-id')[0]
        except:
            order = "no order with that id"

        what = 'invoice'
        # get all item in the cat
        try:
            the_items = getCartItems(request)
            print the_items
        except:
            print "somethting wrong with th items"

        try:
            # check if these is and order
            fullname = unicode(order.first_name) + " " + unicode(order.last_name)
            headers = get_headers()
            seekorder = seekOrder(headers, fullname)
            seekorder = json.loads(seekorder)

            seekorder = seekorder['Invoices']

            if (len(seekorder) == 0):
                print seekorder

                resp = fortnoxOrderandCostumer(request, order, the_items, what)

        except:
            seekorder = "None"

        if (force == '9'):
            print "inforce order"

            resp = fortnoxOrderandCostumer(request, order, the_items, what)
        else:
            print "no force"

    else:
        order = "you are not admin"

    return render_to_response('checkout/consumorder.html', {
        'order': order,
        'seekorder': seekorder
    }, context_instance=RequestContext(request))


def readOrders(request, key):

    if request.user.is_authenticated():

        headers = get_headers()
        seekorders = getOrders(headers)

    else:
        seekorders = "you are not admin"

    return render_to_response('checkout/orders.html', {
        'order': seekorders,
        'seekorder': seekorders
    }, context_instance=RequestContext(request))


def getOrderbyOrderNumerAndCheck(request, order_id):
    if request.user.is_authenticated():
        order = "getting order"
        try:
            order = Checkout.objects.filter(order_number=order_id).order_by('-id')[0]
            order_num = order.order_number
            email = order.email
            pk_order = order.pk
        except:
            order = ''

	try:
            next = Checkout.objects.get(pk=pk_order+1)
	    next_od = next.order_number
        except:
	    next_od = ''

	try:
            prev = Checkout.objects.get(pk=pk_order-1)
            prev_od = prev.order_number
        except:
	    prev_od = ''

        try:
            start = order.message.index('Produkt 1: ') + len('Produkt 1: ')
            end = order.message.index( ' :', start )

            if (len(order.message[start:end]) < 120):
                rea = order.message[start:end].rstrip('\n')
        except:
            rea = 'notrea'

        try:
            start = order.message.index('Totalpris: ') + len('Totalpris: ')
            end = order.message.index( ' SEK', start )
            totalprice = order.message[start:end].rstrip('\n')
        except:
            totalprice = 0

        try:
            start = order.message.index('Frakt och hantering: ') + len('Frakt och hantering: ')
            end = order.message.index( ' SEK', start )
            shipment = order.message[start:end].rstrip('\n')
        except:
            shipment = 0

        try:
            start = order.payment_log.index('Order created in Fortnox: ') + len('Order created in Fortnox: ')
            end = order.payment_log.index( 'fornox order is ok', start )
            json_order = order.payment_log[start:end].rstrip('\n')
        except:
            json_order = {}

        try:
            json_order = json.loads(json_order)
            invoice_number = json_order['Invoice']['DocumentNumber']
            order.total = totalprice
            order.shipment = shipment
        except:
            print "no json"

	try:
	    if (rea == 'rea'):
	        order.reaprice = int(totalprice) * 0.70
		print  order.reaprice
	    else:
	        order.reaprice = 'no rea'
	except:
            print "notrea"

        new_seekorder = {}
        # check get orders
        try:
            headers = get_headers()
            invoice = seekOrderByNumber(headers, invoice_number)
            seekorder = json.loads(invoice)
            new_seekorder['customername'] = seekorder['Invoice']['CustomerName']
            new_seekorder['total'] = seekorder['Invoice']['TotalToPay']
            new_seekorder['invoicetype'] = seekorder['Invoice']['InvoiceType']
            new_seekorder['yourordernumber'] = seekorder['Invoice']['YourOrderNumber']
            new_seekorder['email'] = seekorder['Invoice']['EmailInformation']['EmailAddressTo']

        except:
            seekorder = "None"

    else:
        order = "you are not admin"


    return render_to_response('checkout/dubblecheckconsumorder.html', {
        'order': order,
        'seekorder': new_seekorder,
        'next_od': next_od,
        'prev_od': prev_od
    }, context_instance=RequestContext(request))


def payexCheck2vb(request, payextransactionnumber):
    # check 2 PayEx service
    service = PayEx (
	    merchant_number=settings.PAYEX_MERCHANT_NUMBER,
	    encryption_key=settings.PAYEX_ENCRYPTION_KEY,
	    production=settings.PAYEX_IN_PRODUCTION
	    )

    response = service.check2(
	accountNumber='vamlingbolaget',
	transactionNumber=payextransactionnumber,
	)

    return response


def testklarnahtml(request):
    test_data = get_testcart()
    klarna_order = get_data_defaults(test_data)

    klarna_html = get_order(klarna_order)
    print "hej - testklarnahtml",  klarna_html

    return HttpResponse(klarna_html)

def testconfirmklarnahtml(request):
    print "-----------------------------"
    html = confirm_order('FZE2IG909REESGOSSKHVL3QGUM3')
    print html
    return HttpResponse(html)


def MakeCheckoutTransfer(request, checkout_id):
    # get checkout
    checkout = Checkout.objects.filter(session_key=checkout_id)[0]
    # get corsponding cart
    cart = Cart.objects.get(key = checkout.session_key)
    # and items of that cart
    cartitems = cart.cartitem_set.all()
    reaitems = cart.reacartitem_set.all()
    # Transfer cartitem to checkout
    CheckoutTransfer(checkout, cartitems, reaitems)
    return HttpResponse(status=200)


def ShowCheckouts(request):
    checkouts = Checkout.objects.filter(status='S')

    print checkouts

    return HttpResponse(status=200)



def LookAtDict(request, checkout_order_id):
    checkout = None

    first_order_exist = None
    order_exist = None
    shipping_exist = None

    checkout = Checkout.objects.get(order_number=checkout_order_id)


    try:
        firsTorder = json.loads(checkout.order)
        firstorder = fortnoXobj['Invoice']['YourOrderNumber']
        first_order_exist = True
    except:
        first_order_exist = False



    try:
        fortnoXobj = json.loads(checkout.fortnox_obj)
        orderNum = fortnoXobj['Invoice']['YourOrderNumber']
        order_exist = True
    except:
        order_exist = False



    try:
        unifaunObj = json.loads(checkout.unifaun_obj)
        print unifaunObj
        unifaunNum = unifaunObj
        shipping_exist = True
    except:
        shipping_exist = False

    return render_to_response('checkout/checkout_look.html', {
        'checkout': checkout,
        'orderExist': order_exist,
        'firstOrderExist': first_order_exist,
        'shipping_exist': shipping_exist
    }, context_instance=RequestContext(request))

def CheckoutTransfer(checkout, cartitem, reaitems):
    if (cartitem):
        for item in cartitem:
            orderitem = OrderItem(checkout=checkout, article=item.article, color=item.color, color_2=item.color_2, pattern=item.pattern, pattern_2=item.pattern_2, size=item.size, date_added=item.date_added, quantity=item.quantity, s_type=item.s_type)
            orderitem.save()
    if (reaitems):
        for item in reaitems:
            reaorderitem = ReaOrderItem(checkout=checkout, reaArticle=item.reaArticle, date_added=item.date_added)
            reaorderitem.save()

    log = "Tranfer made from cart to order"
    keepLog('', log, 'INFO', '', checkout.order_number)
