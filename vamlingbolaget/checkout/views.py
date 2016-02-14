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
from fortnox.fortnox import get_headers, get_art_temp, json_update, update_article, CreateCostumer, searchCustomer, customerExistOrCreate, updateCostumer, seekOrder, createOrder, create_invoice_rows, getOrders
import json


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
            msg = "Din order till Vamlingbolaget:\n"
            msg = msg + '--------------------------------- \n'
            msg = msg + 'Din order:\n'
            cart_numberofitems = len(cartitems)
            # create a json object to store order values log and order in json to be used for fortnox integration 
            order_json = {}
			# we have three typ of cart items: cartitems, bargins, rea items that we must loop
            # we also create a json object for fortnox
            order_json['cartitem'] = {}
            for item in cartitems:
                msg = msg + 'Produkt '+ str(i) + ': \n'
                msg = msg +  str(item.quantity) + ' st ' + item.article.name + ' (' + item.article.sku_number + ') '
                products = products + item.article.name
                articles = articles + item.article.sku_number
                payex_products = payex_products + item.article.name
                payex_articles = payex_articles + item.article.sku_number
                order_json['cartitem']['quantity'] =  str(item.quantity)
                order_json['cartitem']['article'] = item.article.sku_number
                if (i != cart_numberofitems):
                    products = products + ', '
                    articles = articles + ', '
                    payex_products = payex_products + ', '
                    payex_articles = payex_articles + ', '
                if (item.pattern_2 != 0):
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' (utsida)\n'
                    msg = msg + 'och ' + item.pattern_2.name + ', ' + item.color_2.name + ' (insida)\n'
                else:
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' \n'
                if (item.article.type.order < 7 or item.article.type.order == 9):
                    msg = msg + 'Storlek: ' + item.size.name + ' \n'

                msg = msg + 'Pris per produkt: ' + str(item.article.price) +  ' SEK \n'
                i = i + 1
            msg = msg + '\n'
            
            # Secondly loop the rea items
            order_json['rea_item'] = {}
            try:
                for item in rea_items:
                    payex_products = "Vamlingbolaget"
                    payex_articles = "Reavaror"        
                    msg = msg + 'Produkt '+ str(i) + str(': rea ') + ': \n'
                    msg = msg +  str(1) + u' st ' +  item.reaArticle.article.name + ' (Rea) : ' + str(item.reaArticle.rea_price)  + ' SEK \n'  
                    msg = msg + 'i ' + item.reaArticle.pattern.name + ', ' + item.reaArticle.color.name + ' \n' 
                    msg = msg + 'Storlek ' + item.reaArticle.size.name + ' \n'            
                    i = i + 1
                    item.id = u'1234'
                    order_json['rea_item']['quantity'] = str(1.00)
                    order_json['rea_item']['article'] = item.reaArticle.article.sku_number
               
                msg = msg + '\n'
            except: 
                pass

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

            # continue to build the message from form values
            msg = msg + 'Frakt och hantering: '+ str(handling) +' SEK \n'
            msg = msg + '--------------------------------- \n'
            msg = msg + 'Totalpris: %s SEK \n' %str(totalprice)
            msg = msg + '--------------------------------- \n'
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
            msg = msg + '* En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. \n'

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
                new_order.payment_log = '* Pay on Delivery - Sending Mail order to ' + request.POST['email']

                # json order for fortnox
                new_order.order = json.dumps(order_json)
                new_order.save()

                to = [request.POST['email'], 'info@vamlingbolaget.com']
                if (first_name == "Tester"):
                    print "this is for testing we don not need to send a email"
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
                new_order.payment_log = '* Card payment Log - Payment request sent, payEx key: ' + str(PayExRefKey) 
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
                order.payment_log = order.payment_log + u'Log Success: Checkout found with the payex_key: ' +  orderref + '\n' + 'cartid: ' + cart_id
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
                    transnumber = response['transactionNumber']
                    order.message = order.message + 'PayEx transaktion: ' + str(transnumber) + '\n'
                    order.payment_log = order.payment_log + '\n' + '3: Log Success: PayEx transaktion: ' + str(transnumber)
                    order.status = 'P'                  
                except:
                    order.payment_log = order.payment_log + '\n' + '3: Log Fail, PayEx transaktion not found: ' + str(transnumber)

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
        order = Checkout.objects.filter(session_key=cart_id)[0]
    except:
       order = 1
       
    if (order != 1):
        try: 
            order.payment_log = order.payment_log + "* Sending thanks message" + '\n'
            order.save()
        except:
            order.payment_log = order.payment_log + "* can find order" + '\n'
            order.save()    
              
        message = "Tack for din order"

    else:
        message = u"Lägg till något i din shoppinglåda och gör en beställning."
 
    return render_to_response('checkout/thanks.html', {
        'order': order,
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
        order.payment_log = order.payment_log + '\n' + '4; Payex callback Log: PayEx transaktionNumber, transactionRef: ' + str(transactionNumber) + ', ' + str(transactionRef) + ' orderRef: ' + str(orderRef) + ', from ip: '+ ip + '\n'

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
            order.payment_log = order.payment_log +  '\n' + 'Duplicate order nummer'
    
        # fortnox log 
   
        order.payment_log = order.payment_log +  '\n' + 'Fortnox callback Log: order id: ' + str(order_id) + ', from ip: '+ ip 
        order.save()
       
        if (ip == order.ip):
             order.payment_log = order.payment_log +  '\n' + 'Fortnox callback Log: ip from order to order is the same'
             order.save()
        else: 
             order.payment_log = order.payment_log +  '\n' + 'Fortnox callback Log: ip from order to order is not the same'
             order.save()

        # get all item in the cat
        try:
            the_items = getCartItems(request)
            print the_items
        except:
            print "somethting wrong with th items"

        # create order in fortnox
        print "fortnox"
        try: 
            json_order = order.order         
            fortnoxOrderandCostumer(request, order, the_items)
            order.payment_log = order.payment_log +  '\n' + 'fornox order is ok'
            order.save()
        except: 
            order.payment_log = order.payment_log +  '\n' + 'something wrong with fortnox'
            order.save()

        # set the new stock
        print "stock" 
        print the_items
        try: 
            cleanCartandSetStock(request, the_items)

            order.payment_log = order.payment_log +  '\n' + 'cleaning cart' 
            order.save()
        except: 
            order.payment_log = order.payment_log +  '\n' + 'error cleaning cart'
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
            print "loop !"
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
    try: 
        order_json = json.loads(order_json)
    except: 
        pass 

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
        customer_no = customerExistOrCreate(headers, customer)
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox customer: ' +  str(customer_no)
        new_order.save()
    except: 
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox customer not resolved' 
        new_order.save()

    comments = "payexid: " + unicode(new_order.payex_key)
    print comments
   
    # Creat the order part of the json from order_json and log 
    try: 
        invoice_rows = create_invoice_rows(order_json)
        new_order.payment_log = new_order.payment_log +  '\n' + str(invoice_rows)
        new_order.save()
    except: 
        new_order.payment_log = new_order.payment_log +  '\n' + 'Fortnox order json not resolved' 
        new_order.save()

    # add addtional information to json
    orderid_ = new_order.order_number 
    customer_order = json.dumps({
                "Invoice": {
                    "InvoiceRows": invoice_rows,
                    "CustomerNumber": customer_no, 
                    "PriceList": "B",
                    "Comments": comments,
                    "YourOrderNumber": orderid_,
                }
            })  
    # send the json order, log and save the order 
    try: 
        order = createOrder(headers, customer_order)
        new_order.payment_log = new_order.payment_log +  '\n' + 'Order created in Fortnox: ' +  str(order)
        new_order.save()

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
            print "copy" 
            tempprice = 0

        old_email = email

        if (rea == 'rea'): 
            try:
                start = order.message.index('Totalpris: ') + len('Totalpris: ')
                end = order.message.index( ' SEK', start )
                if (len(order.message[start:end]) < 120):
                    tempprice = order.message[start:end].rstrip('\n')    
                    print tempprice       
            except: 
                tempprice = 0
                
        total = total + int(tempprice)
        print total

        l = l - 1 
        print l
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
            order =  Checkout.objects.filter(order_number=order_id).order_by('-id')[0] 

        except: 
            order = "no order with that id"
        try:
            # check if these is and order  
            fullname = unicode(order.first_name) + " " + unicode(order.last_name)
            headers = get_headers()
            seekorder = seekOrder(headers, fullname)
            seekorder = json.loads(seekorder)

            seekorder = seekorder['Invoices']

            # get all item in the cat
            try:
                the_items = getCartItems(request)
                print the_items
            except:
                print "somethting wrong with th items"

            if (len(seekorder) == 0):
                order_json = order.order
                resp = fortnoxOrderandCostumer(request, order, the_items)

        except: 
            seekorder = "None"

        if (force == '9'): 
            print "inforce order"
            order_json = order.order
            resp = fortnoxOrderandCostumer(request, order,  the_items)
            print resp
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


