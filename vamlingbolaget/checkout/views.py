#-*-coding:utf-8-*-

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core import mail
from cart.views import _cart_id, totalsum, _new_cart_id, getnames

from cart.models import Cart, CartItem
from forms import CheckoutForm
from models import Checkout
import random
from payex.service import PayEx

def checkout_test(request):
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)
    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    getnames(cartitems)
    returntotal = totalsum(cartitems, bargains)
    totalprice = returntotal['totalprice']
    totalitems = returntotal['totalitems']
    handling = returntotal['handling']
    form = CheckoutForm()
    returntotal['form'] = form


    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.ip = request.META['REMOTE_ADDR']
            new_order.status = 'O'
            paymentmethod = request.POST['paymentmethod']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            street = request.POST['street']
            postcode = request.POST['postcode']
            city = request.POST['city']
            if (request.POST['country']):
                country = request.POST['country']
            else:
                country = 'none'
            if (request.POST['message']):
                message = request.POST['message']
            else:
                message = 'none'
            i = 1
            products = 'Vamlingbolaget: '
            articles = 'Artikel nummer: '
            msg = "Din order till Vamlingbolaget:\n"
            msg = msg + '--------------------------------- \n'
            msg = msg + 'Din order:\n'
            cart_numberofitems = len(cartitems)
            for item in cartitems:
                msg = msg + 'produkt '+ str(i) + ': \n'
                msg = msg +  str(item.quantity) + ' st ' + item.article.name + ' (' + item.article.sku_number + ') '
                products = products + item.article.name
                articles = articles + item.article.sku_number
                if (i != cart_numberofitems):
                    products = products + ', '
                    articles = articles + ', '
                if (item.pattern_2 != 0):
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' (utsida)\n'
                    msg = msg + 'och ' + item.pattern_2.name + ', ' + item.color_2.name + ' (insida)\n'
                else:
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' \n'
                if (item.article.category.order < 3):
                    msg = msg + 'Storlek: ' + item.size.name + ' \n'

                msg = msg + 'Pris per produkt: ' + str(item.article.price) +  ' SEK \n'
                i = i + 1
            msg = msg + '\n'
            msg = msg + 'Frakt och hantering: 50 SEK \n'
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
            if (message != 'none'):
                msg = msg + 'Din Meddelande:\n'
                msg = msg + u' %s \n' % (message)
                msg = msg + '\n'
            msg = msg + '--------------------------------------------------------------------------------- \n'
            msg = msg + ' \n'
            msg = msg + '* En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. \n'

            if (paymentmethod == 'P'):
                msg = msg + '* Du betalar med postforskatt. \n'
            if (paymentmethod == 'C'):
                msg = msg + '* Du har valt kortbetalning. \n'

            msg = msg + '- Tack!\n'
            order_numb = random.randrange(0, 111111, 3)
            new_order.order_number = order_numb
            msg = msg + '--------------------------------------------------------------------------------- \n'
            msg = msg + 'Ditt ordernummer: '+ str(order_numb) +'\n'

            new_order.session_key = _cart_id(request)

            new_order.paymentmethod = paymentmethod

            if (paymentmethod == 'P'):
                new_order.save()
                to = [request.POST['email'], 'info@vamlingbolaget.com']
                mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %msg, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)
                return HttpResponseRedirect('thanks/')

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
                    productNumber=products,
                    description=articles,
                    clientIPAddress=new_order.ip,
                    clientIdentifier='USERAGENT=test&username=testuser',
                    additionalValues='',
                    returnUrl='http://www.vamlingbolaget.com/checkout/success',
                    view='CREDITCARD',
                    cancelUrl='http://www.vamlingbolaget.com/checkout/cancel'
                )

                PayExRefKey = response['orderRef']

                new_order.payex_key = PayExRefKey
                new_order.order = msg
                new_order.message = new_order.message + '\n' + u'1 :Payment Log: Payment request sent.'
                new_order.save()
                return HttpResponseRedirect(response['redirectUrl'])

    return render_to_response('checkout/checkout_test.html', {
        'form': form,
        'totalprice': totalprice,
        'totalitems': totalitems,
        'handling': handling,
        'cartitems': cartitems,
        'bargains' : bargains,

        },
        context_instance=RequestContext(request))

def success(request):
    # if payex Transaction was successfully performed

    service = PayEx(
        merchant_number=settings.PAYEX_MERCHANT_NUMBER,
        encryption_key=settings.PAYEX_ENCRYPTION_KEY,
        production=settings.PAYEX_IN_PRODUCTION
    )
    try:
        orderref = request.GET.get('orderRef', None)

    except:
        pass

    if orderref:
        response = service.complete(orderRef=orderref)
        if (response['status']['errorCode'] == 'OK' and response['transactionStatus'] == '0'):
            cart_id = _cart_id(request)
            try:
                order = Checkout.objects.get(payex_key=orderref)
            except:
                order = 1

            if (order == 1):
                message = u'Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com.'
                return render_to_response('checkout/thanks.html', {
                    'message': message,
                }, context_instance=RequestContext(request))

            if (order != 1 and order.status == 'O'):
                cart = Cart.objects.get(key = cart_id)
                cartitems_key = cart.id
                cartitems = CartItem.objects.filter(cart = cartitems_key)
                cartitems.delete()
                cart.delete()
                _new_cart_id(request)
                message = "Tack for din order"
                order.message = order.message + '\n' + u'2: Log Success: old cart removed'

                try:
                    transnumber = response['transactionNumber']
                    order.order = order.order + 'PayEx transaktion: ' + str(transnumber) + '\n'
                    order.message = order.message + '\n' + '3: Log Success, PayEx transaktion: ' + str(transnumber)
                except:
                    pass
                #to = [order.email, 'info@vamlingbolaget.com']
                #mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %order.order, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)

                order.order = order.order + u'Om du har frågor kontakta oss på telefonnummer 0498-498080 eller skicka ett mail till info@vamlingbolaget.com.'
                order.status = 'P'
                order.message = order.message + '\n' + u'4: Log Success: Mail sent to mail adress : ' + order.email

                order.save()

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
                return render_to_response('checkout/thanks.html', {
                'message': message,
                }, context_instance=RequestContext(request))
            else:
                order.message = order.message + '\n' + u'2: Cancel log: "- Betalningen avslogs eller avbröts.'
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


def cancel(request):
    # fill the form with the same info
    return HttpResponseRedirect('/checkout/')

def thanks(request):
    cart_id = _cart_id(request)

    try:
        order = Checkout.objects.get(session_key=cart_id)
    except:
        order = 1
    if (order != 1):
        order.message = order.message + '\n' + '5: Log Thanks: thank you message displayed.'

        order.save()
        _new_cart_id(request)
        message = "Tack for din order"

    else:
        message = u"Lägg till något i din shoppinglåda och gör en beställning."
        return render_to_response('checkout/thanks.html', {
            'message': message
        }, context_instance=RequestContext(request))

    return render_to_response('checkout/thanks.html', {
        'order': order,
        'message': message
    }, context_instance=RequestContext(request))

def checkout(request):
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)
    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    getnames(cartitems)
    returntotal = totalsum(cartitems, bargains)
    totalprice = returntotal['totalprice']
    totalitems = returntotal['totalitems']
    handling = returntotal['handling']
    form = CheckoutForm()
    returntotal['form'] = form

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.ip = request.META['REMOTE_ADDR']
            new_order.status = 'O'
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            street = request.POST['street']
            postcode = request.POST['postcode']
            city = request.POST['city']
            if (request.POST['country']):
                country = request.POST['country']
            else:
                country = 'none'
            if (request.POST['message']):
                message = request.POST['message']
            else:
                message = 'none'
            i = 1
            msg = "Din order till Vamlingbolaget:\n"
            msg = msg + '--------------------------------- \n'
            msg = msg + 'Din order:\n'
            for item in cartitems:
                msg = msg + 'produkt '+ str(i) + ': \n'
                msg = msg +  str(item.quantity) + ' st ' + item.article.name + ' (' + item.article.sku_number + ') '

                if (item.pattern_2 != 0):
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' (utsida)\n'
                    msg = msg + 'och ' + item.pattern_2.name + ', ' + item.color_2.name + ' (insida)\n'
                else:
                    msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' \n'

                if (item.article.category.order < 4):
                    msg = msg + 'Storlek: ' + item.size.name + ' \n'
                elif (item.article.category.order == 5):
                    msg = msg + 'Antal meter: ' + str(item.quantity) + ' \n'
                else:
                    msg = msg

                if (item.article.category.order < 4):
                    msg = msg + 'Pris per produkt: ' + str(item.article.price) +  ' SEK \n'
                elif (item.article.category.order == 5):
                    msg = msg + 'Pris per meter: ' + str(item.article.price) +  ' SEK \n'
                else:
                    msg = msg + 'Pris per produkt: ' + str(item.article.price) +  ' SEK \n'

                i = i + 1


            msg = msg + '\n'
            msg = msg + 'Frakt och hantering: 50 SEK \n'
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
            if (message != 'none'):
                msg = msg + 'Din Meddelande:\n'
                msg = msg + u' %s \n' % (message)
                msg = msg + '\n'
            msg = msg + '--------------------------------------------------------------------------------- \n'
            msg = msg + ' \n'
            msg = msg + '* En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. \n'
            msg = msg + '* Du betalar med postforskatt \n'
            msg = msg + '- Tack!'
            new_order.order_number = random.randrange(0, 111111, 3)
            new_order.session_key = _cart_id(request)
            new_order.order = msg
            new_order.save()
            to = [request.POST['email'], 'info@vamlingbolaget.com']
            mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %msg, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)

            return HttpResponseRedirect('thanks/')

    return render_to_response('checkout/checkout.html', {
        'form': form,
        'totalprice': totalprice,
        'totalitems': totalitems,
        'handling': handling,
        'cartitems': cartitems,
        'bargains' : bargains,

        },
        context_instance=RequestContext(request))

def payexCallback(request):
    #  transactionRef =<String(32)>&transactionNumber=<Integer(7-9)>&orderRef=<String(32)>
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
        order.message = order.message + '\n' + '4; Payex callback Log: PayEx transaktionNumber: ' + str(transactionNumber) + ' orderRef: ' + str(orderRef) +'\n'
        print order.message
        order.save()

    return HttpResponse(status=200)