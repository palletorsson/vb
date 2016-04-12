#-*-coding:utf-8-*-

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core import mail
from cart.views import _cart_id, totalsum, _new_cart_id, getnames 
from products.models import ReaArticle
from cart.models import Cart, CartItem
from forms import CheckoutForm
from models import Checkout
import random
from payex.service import PayEx
from fortnox.fortnox import get_headers, get_art_temp, json_update, update_article, CreateCostumer, searchCustomer, customerExistOrCreate, updateCostumer, seekOrder, createOrder, create_invoice_rows, getOrders, seekOrderByNumber, formatJson
import json
import time
import datetime
from translator import toEnglish

# --> from /checkout/ pay --> with card | on delivery   
def checkout(request):
    # get the all cart data 
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)
    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    try: 
        rea_items = cart.reacartitem_set.all()
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


    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # start the order process and store form values 
            new_order = form.save(commit=False)
            new_order.ip = request.META['REMOTE_ADDR']
            new_order.status = 'O'
            paymentmethod = request.POST['paymentmethod']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            street = request.POST['street']
            postcode = request.POST['postcode']
            city = request.POST['city']
            sms = request.POST['sms']

            # optional values need and if check 
            if (request.POST['phone']):
                phone = request.POST['phone']
            else:
                phone = 'none'
  
            if (request.POST['country']):
                country = request.POST['country']
            else:
                country = 'none'
            if (request.POST['message']):
                message = request.POST['message']
            else:
                message = 'none'

            # set parameters for the costumer message to be created 
            i = 1
            products = 'Vamlingbolaget: '
            articles = 'Artikel nummer: '
            payex_articles = ''
            payex_products = ''

            # start creating the costumer message 
            message_header = "Din order till Vamlingbolaget:\n--------------------------------- \nDin order: \n"
            msg = message_header

            cart_numberofitems = len(cartitems)
            # create a json object to store order values log and order in json to be used for fortnox integration 
            order_json = {}
			# we have three typ of cart items: cartitems, bargins, rea items that we must loop
            # we also create a json object for fortnox
            order_json['cartitems'] = {}
            temp_cartitems = []
            cartitemexist = 0; 
            reaitemexist = 0;

            for item in cartitems:
                cartitemexist = 1; 
                msg = msg + 'Produkt '+ str(i) + ': \n'
                msg = msg +  str(item.quantity) + ' st ' + item.article.name + ' (' + item.article.sku_number + ') '
                products = products + item.article.name
                articles = articles + item.article.sku_number
                payex_products = payex_products + item.article.name
                payex_articles = payex_articles + item.article.sku_number
                temp_cartitems.append(
        			{'quantity':str(item.quantity), 
        			 'article': item.article.sku_number,
        			 'color': item.color.name, 
        			 'pattern': item.pattern.name })
		
                if (i != cart_numberofitems):
                    products = products + ', '
                    articles = articles + ', '
                    payex_products = payex_products + ', '
                    payex_articles = payex_articles + ', '
                if (item.pattern_2 != 0):
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' (utsida)\n'
                    msg = msg + 'och ' + item.pattern_2.name + ', ' + item.color_2.name + ' (insida)\n'
                    #order_json['cartitem'][i]['color2'] = item.color_2.name
                    order_json['cartitem'][i]['patter2'] = item.patter_2.name
                else:
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' \n'
		    
                if (item.article.type.order < 7 or item.article.type.order == 9):
                    msg = msg + 'Storlek: ' + item.size.name + ' \n'

                msg = msg + 'Pris per produkt: ' + str(item.article.price) +  ' SEK \n'
	
            order_json['cartitems'] = temp_cartitems
            # Secondly loop the rea items
            order_json['rea_items'] = {}
	    
            temp_reaitems = []
            try:
                for item in rea_items:
                    reaitemexist = 1; 
                    payex_products = "Vamlingbolaget"
                    payex_articles = "Reavaror"        
                    msg = msg + 'Produkt, '+ str(i) + str(' Rea:') + ': \n'
                    msg = msg +  str(1) + u' st ' +  item.reaArticle.article.name + ' (Rea) : ' + str(item.reaArticle.rea_price)  + ' SEK \n'  
                    msg = msg + 'i ' + item.reaArticle.pattern.name + ', ' + item.reaArticle.color.name + ' \n' 
                    msg = msg + 'Storlek: ' + item.reaArticle.size.name + ' \n'            
                    i = i + 1
                    item.id = u'1234'
                    temp_reaitems.append(
        			{'quantity':str(1.00), 
        			 'article': item.reaArticle.article.sku_number,
        			 'color': item.reaArticle.color.name, 
        			 'pattern': item.reaArticle.pattern.name, 
        			 'rea': 'rea' })		   
                msg = msg + '\n'


            except: 
                pass
            
            order_json['rea_items'] = temp_reaitems
            # also create a place holder for pax transactionnumber
            order_json['transnumber'] = 'placeholder'
	    
            # and lastly bargins (this is actuality an old model we can consider removing)
            order_json['bargains'] = {}
            for item in bargains:
                payex_products = "Vamlingbolaget"
                payex_articles = "Reavaror"        
                msg = msg + 'Produkt '+ str(i) + str(': fynd ') + ': \n'
                msg = msg +  str(1) + u' st ' +  item.bargain.title + ' : ' + str(item.bargain.price)  + ' SEK \n' 
                msg = msg + u' ( ' + item.bargain.description  + ' ) \n'            
                i = i + 1
                item.id = u'2345'
                order_json['bargains']['quantity'] = 1
                order_json['bargains']['article'] = 1
               
            msg = msg + '\n'

            # if the payex_products string get to long we will just call it Vamlingbolaget, the same goes for payex_articles string
            if len(payex_products) > 30:
                payex_products = "Vamlingbolaget"

            if len(payex_articles) > 30:
                payex_articles = "Flera artiklar"

            # continue to build summery of the message from form values
            msg = msg + 'Frakt och hantering: '+ str(handling) +' SEK \n'
            msg = msg + '--------------------------------- \n'
            msg = msg + 'Totalpris: %s SEK \n' %str(totalprice)
            msg = msg + '--------------------------------- \n'
            msg = msg + '\n'
            msg = msg + 'Din adress:  \n'
            msg = msg + u'%s %s \n' % (first_name, last_name)
            msg = msg + u'%s \n' % (street)
            msg = msg + u'%s %s \n' % (postcode, city)
            if (country != 'none'):
                msg = msg + u'%s \n' % (country)
            msg = msg + '--------------------------------- \n'

            if (phone != 'none'):
                msg = msg + u'Ditt telefonnummer: %s \n' % (phone)
                msg = msg + '--------------------------------- \n'

            if (message != 'none'):
                msg = msg + 'Din Meddelande:\n'
                msg = msg + u' %s \n' % (message)
                msg = msg + '\n'
            msg = msg + '--------------------------------------------------------------------------------- \n'
            if (cartitemexist == 1): 
                msg = msg + '* En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. \n'
            if (reaitemexist == 1):
                msg = msg + '* En reaorder till Vamlingbolaget tar ca 1 veckor. \n'  
                              
            # check it the method is to pay --> with card | on delivery  
            if (paymentmethod == 'P'):
                msg = msg + u'* Du betalar med postförskott. \n'
            if (paymentmethod == 'C'):
                msg = msg + u'* Du har valt kortbetalning. \n'

            # check if the costumer checked the sms box in the from 
            if (sms == 'yes'):
                msg = msg + '--------------------------------------------------------------------------------- \n'
                msg = msg + u'* Du får en sms-avisering. \n'

            msg = msg + '- Tack!\n'

            # create a random referance number
            order_numb = random.randrange(0, 111111, 3)

            # create a new order
            new_order.order_number = order_numb
            msg = msg + '--------------------------------------------------------------------------------- \n'
            msg = msg + 'Ditt ordernummer: '+ str(order_numb) +'\n'

            new_order.session_key = _cart_id(request)

            new_order.paymentmethod = paymentmethod

            # if costumer pay on delivery 
            # we just send and email with order to vamlingbolaget and a copy to the coustumer and redirect to the thanks url
            # we also save the order in json that we can use with fortnox, as well as staring the payment log 
            if (paymentmethod == 'P'):
                # save message
                new_order.message = msg

                # start payment log
                new_order.payment_log = 'Log Email. Pay on Delivery - Sending Mail order to ' + request.POST['email'] + '\n'

                # json order for fortnox
                new_order.order = json.dumps(order_json)
                new_order.save()

                to = [request.POST['email'], 'info@vamlingbolaget.com']
                if (first_name == "Tester"):
                    print "this is for testing we don not need to send a email"
                    enmsg = toEnglish(msg)
                    print enmsg 
                else:  
                    mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %msg, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)

                return HttpResponseRedirect('thanks/')


            # if costumer pay with card we need to start a PayEx service
            if (paymentmethod == 'C'):
                # Initialize PayEx service
                service = PayEx(
                    merchant_number=settings.PAYEX_MERCHANT_NUMBER,
                    encryption_key=settings.PAYEX_ENCRYPTION_KEY,
                    production=settings.PAYEX_IN_PRODUCTION
                    )

                price = totalprice * 100

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
                new_order.message = msg
                new_order.payment_log = '1 Card payment Log - Payment request sent, payEx key: ' + str(PayExRefKey) 
                new_order.order = order_json 
                new_order.save()
                return HttpResponseRedirect(response['redirectUrl'])

    return render_to_response('checkout/checkout.html', {
        'form': form,
        'totalprice': totalprice,
        'totalitems': totalitems,
        'handling': handling,
        'cartitems': cartitems,
        'bargains' : bargains,
        'rea' : rea_items,
        'sweden': sweden,
        'voucher': voucher,
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
        print "no payex_key found"

    if orderref:
        response = service.complete(orderRef=orderref)

		# if we get a good responce from sevice complite         
        if (response['status']['errorCode'] == 'OK' and response['transactionStatus'] == '0'):

            # get cart id from request
            cart_id = _cart_id(request)
            
            # get the checkout 
            try:
                order = Checkout.objects.get(payex_key=orderref)
                order.payment_log = order.payment_log + u'Log Success: Checkout found with the payex_key: ' +  orderref + ' Cartid: ' + cart_id + '\n'
            except:
                order = 1
                print 'Log Error: no checkout found with the payex_key: ' + str(orderref)

            # in the unlily event that the checkout can't be found send a coustmer to thanks url with a message to contact vamlingbolaget.  
            if (order == 1):
                message = u'Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com.'
                return render_to_response('checkout/thanks.html', {
                    'message': message,
                }, context_instance=RequestContext(request))

            # remove the old cart and cart items if status is Order 
            if (order != 1 and order.status == 'O'):

                try:
                    transnumber_ = response['transactionNumber']
                    print "--------------------------------------", transnumber_
                    print "--------------------------------------", order.order
                    order_obj = formatJson(order.order)
                    print "--------------------------------------", order_obj
                    order_obj = json.loads(order_obj)
                    print "--------------------------------------", order_obj
                    order_obj["transnumber"] = str(transnumber_)
                    print "--------------------------------------", order_obj["transnumber"] 
                    print "--------------------------------------", order_obj
                    order.order = order_obj
                    order.save()
                    order.payment_log = order.payment_log + 'Log Trans: Adding transnumber' + str(transnumber_) + '\n' 
                    order.save()
                except:
                    order.payment_log = order.payment_log + 'Log Trans: Fail, transnumber' + '\n' 
                    order.save()

                try:
                    transnumber = response['transactionNumber']
                    order.message = order.message + 'PayEx transaktion: ' + str(transnumber) + '\n'
                    order.payment_log = order.payment_log + 'Log Success: PayEx transaktion: ' + str(transnumber) + '\n'
                    order.status = 'P'   
                    order.save()               
                except:
                    order.payment_log = order.payment_log  + 'Log Success Fail, PayEx transaktion not found: ' + str(transnumber) + '\n'
                    order.save()
                try:
                    to = [order.email, 'info@vamlingbolaget.com']
                    mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %order.message, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)
                    order.message = order.message + u'Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com.'
                    order.payment_log = order.payment_log + '\n' + u'4: Log Success: Mail sent to mail adress : ' + order.email
                    order.save()
                except: 
                    order.payment_log = order.payment_log + '\n' + u'4: Log Fail: Mail not sent to mail adress : ' + str(order.email)


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
                order.payment_log = order.payment_log + '\n' + u'2: Cancel log: - det fanns ingen beställning att avbryta'

                message = u"- Det finns inte någon sådan beställning"
                return render_to_response('checkout/thanks.html', {
                'message': message,
                }, context_instance=RequestContext(request))

            else:
                order.payment_log = order.payment_log + '\n' + u'2: Cancel log: - Betalningen avslogs eller avbröts.'
                order.status = 'C'
                order.save()
                message = u"- Betalningen avslogs eller avbröts."

            return render_to_response('checkout/thanks.html', {
                'message': message,
                'cancel':1,
            }, context_instance=RequestContext(request))
    else:
        message = "Skicka en order eller utforska utbudet"
        return render_to_response('checkout/thanks.html', {
            'message': message
        }, context_instance=RequestContext(request))

# if payment cancelde
def cancel(request):
    cart_id = _cart_id(request)
    try:
        order = Checkout.objects.get(session_key=cart_id)
    except:
        order = 0

    if(order == 0):
        pass
    else:
        order.payment_log = order.payment_log + '\n' + 'Payment canceled' 

    return HttpResponseRedirect('/checkout/')

def thanks(request):
    cart_id = _cart_id(request)

    try:
        checkout = Checkout.objects.filter(session_key=cart_id)[0]
    except:
        checkout = 1
       
    if (checkout != 1):
        try:
            checkout.payment_log = checkout.payment_log + "Log Thanks: Sending thanks message OK" + '\n'
            checkout.save()
        except:
            checkout.payment_log = checkout.payment_log + "Log Thanks: can not find order" + '\n'
            checkout.save()    
              
        message = "Tack for din order"
        
    else:
        message = u"Lägg till något i din shoppinglåda och gör en beställning."
    
    return render_to_response('checkout/thanks.html', {
        'order': checkout,
        'message': message
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
        order.payment_log = order.payment_log + '4; Payex callback Log: PayEx transaktionNumber, transactionRef: ' + str(transactionNumber) + ', ' + str(transactionRef) + ' orderRef: ' + str(orderRef) + ', from ip: '+ ip + '\n'
        order.save()

    return HttpResponse(status=200)


def fortnox(request): 

    try:
        ip = request.META['REMOTE_ADDR']
    except:
        ip = 'None'

    try: 
        order_id = request.POST['order_id']
    except: 
        order_id = 0

    if (order_id != 0):
        try: 
            order = Checkout.objects.get(order_number=order_id) 
        except: 
            order = Checkout.objects.filter(order_number=order_id) 
            order = order.reverse()[0]
            order.payment_log = order.payment_log + 'Duplicate order nummer' +  '\n' 
            order.save()    
        
        order.payment_log = order.payment_log + 'Fortnox callback Log: order id: ' + str(order_id) + ', from ip: '+ ip  + '\n' 
        order.save()
       
        if (ip == order.ip):
             order.payment_log = order.payment_log + 'Fortnox callback Log: ip from order to order is the same' + '\n'
             order.save()
        else: 
             order.payment_log = order.payment_log + 'Fortnox callback Log: ip from order to order is not the same' + '\n' 
             order.save()

        # get all item in the cat
        try:
            the_items = getCartItems(request)
        except:
            order.payment_log = order.payment_log + 'Error, cartitems' + '\n'
            order.save()    

        # create order in fortnox
        try: 
            json_order = the_items     
            fortnoxOrderandCostumer(request, order, json_order)
            order.payment_log = order.payment_log + 'fornox order is ok' + '\n'
            order.save()
        except: 
            order.payment_log = order.payment_log + 'something wrong with fortnox' + '\n'
            order.save()

        # set the new stock
        try: 
            cleanCartandSetStock(request, the_items)

            order.payment_log = order.payment_log + 'cleaning cart' + '\n'
            order.save()
        except: 
            order.payment_log = order.payment_log + 'error cleaning cart' + '\n' 
            order.save()

        return HttpResponse(status=200)
    else: 
        return HttpResponseRedirect('/')


# clean cart and chang stockquanity 
def cleanCartandSetStock(request, the_items): 
 
    # get cart, key and items 

    # update rea stock internalty 
    cartitems = the_items['cartitems'] 
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
 
    # remove all caritem from that cart and the cart 
    cartitems.delete() 
    bargains.delete()
    try: 
        rea_items.delete()
    except:
        pass 

    voucher.delete()
    cart.delete()

    # create a clean new cart
    _new_cart_id(request)

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

# Run after order when customer is send to conferm url /thanks/
def fortnoxOrderandCostumer(request, new_order, order_json):

    fullname = unicode(new_order.first_name) + " " + unicode(new_order.last_name)
    
    customer_no = '0'

    headers = get_headers()

    customer = json.dumps({
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

    # To make an Fortnox order we need a Custumer
    # first check if customer exist 
    # and update or create customer and get customer number back and log
    try:
        customer_no = customerExistOrCreate(headers, customer, order_json)
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox customer ok ' 
        new_order.save()
    except: 
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox customer not resolved' 
        new_order.save()

    try: 
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        new_order.payment_log = new_order.payment_log +  '\n' + str(st) 
        new_order.save()
    except: 
        pass

    # Creat the order part of the json from order_json and log 
    try:         
        invoice_rows = create_invoice_rows(order_json)
        new_order.payment_log = new_order.payment_log +  '\n' +  'Invoice_rows worked ' 
        new_order.save()
    except: 
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox order json not resolved' 
        new_order.save()

    # add addtional information to comment  and invoice type feilds
    try:
        orderid_ = new_order.order_number 
        comments = "Order number: " + unicode(orderid_)
    except:
        comments = ""

    invoice_type = new_order.paymentmethod
    
    if(invoice_type == 'P'): 
        invoice_type_value = 'INVOICE'
    else:
        invoice_type_value = 'CASHINVOICE'

        try: 
            order_obj = json.loads(new_order.order)
            tranid = order_obj['transnumber']
            comments = comments + " Payextransactionnumber: " + unicode(tranid) 
        except: 
            pass 

        try: 
            comments = comments + " Payexkey: " + unicode(new_order.payex_key) 
        except:
            pass 

    customer_order = json.dumps({
                "Invoice": {
                    "InvoiceRows": invoice_rows,
                    "CustomerNumber": customer_no, 
                    "PriceList": "B",
                    "Comments": comments,
                    "YourOrderNumber": orderid_,
                    "InvoiceType": invoice_type_value, 
                }
            })  
    # send the json order, log and save the order 
    try: 
        return_order = createOrder(headers, customer_order)

        new_order.payment_log = new_order.payment_log +  '\n' + 'Order created in Fortnox: ' +  str(return_order)
        new_order.save()
        retun_order_json = json.loads(return_order)
    except: 
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox order not created' 
        new_order.save()

    # save create new blank order  
    new_order.save()

    return 1  

# to show all checkouts
def admin_view(request, limit):
    orders = Checkout.objects.all().order_by('-id')[:limit]   
    for order in orders:
        try:
            start = order.order.index(' st ') + len(' st ')
            end = order.order.index( ' i ', start )
            if (len(order.order[start:end]) < 120):
                order.art = order.order[start:end]     
        except: 
            pass
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
    return render_to_response('checkout/admin_view.html', {
        'orders': orders
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
    message = cleanCartandSetStock(request)

    return render_to_response('checkout/tests.html', {
        'message': message
    }, context_instance=RequestContext(request))


def consumOrder(request, order_id, force):
    if request.user.is_authenticated():  
        try:   
            order = Checkout.objects.filter(order_number=order_id).order_by('-id')[0] 

        except: 
            order = "no order with that id"

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

                resp = fortnoxOrderandCostumer(request, order, the_items)

        except: 
            seekorder = "None"

        if (force == '9'): 
            print "inforce order"

            resp = fortnoxOrderandCostumer(request, order, the_items)
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
    

