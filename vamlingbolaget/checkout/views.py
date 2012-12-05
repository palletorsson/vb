# -*- coding: utf8 -*- 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from cart.views import _cart_id, totalsum,  _new_cart_id
            
from cart.models import Cart
from forms import CheckoutForm
from models import Checkout
import random

def checkout(request):
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)
    cartitems = cart.cartitem_set.all()
    returntotal = totalsum(cartitems)
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
            msg = "> ORDER:\n"
            i = 1
            for item in cartitems:
                msg = msg + '>> ' + item.article.name + ' (' + item.article.sku_number + ') \n'
                msg = msg + '>> i ' + item.pattern.name + ', ' + item.color.name + ' \n'
                msg = msg + '>> Antal : ' + str(item.quantity) + ' \n'
                msg = msg + '>> Pris per plagg: ' + str(item.article.price) +  ' SEK \n'
                i = i + 1

            msg = msg + '------------------------------------------------------\n'
            msg = msg + '>> Frakt och Hantering: 40 SEK \n'
            msg = msg + '------------------------------------------------------\n'
            msg = msg + '>>> Totalpris: ' + str(totalprice) +  ' SEK \n'


            new_order.order_number = random.randrange(0, 111111, 3)
            new_order.session_key = _cart_id(request)
            new_order.order = msg
            new_order.save()

            send_mail('Din beställning från Vamlingbolaget', 'Tack för din beställning, den är som följer \n %s' %msg, '23ctest@gmail.com', [request.POST['email']])

            return HttpResponseRedirect('thanks/')

    return render_to_response('checkout/checkout.html', {
        'form': form,
        'totalprice': totalprice,
        'totalitems': totalitems,
        'handling': handling,
        'cartitems': cartitems,
        },
        context_instance=RequestContext(request))

def thanks(request):
    cart_id = _cart_id(request)
    try:
        order = Checkout.objects.get(session_key=cart_id)
    except:
        order = 1
    if (order != 1):
        cart = Cart.objects.filter(key = cart_id)
        cart.delete()
        _new_cart_id(request)
        message = "Tack for din order"
    else:
        message = "Skicka en order"
        return render_to_response('checkout/thanks.html', {
            'message': message
        }, context_instance=RequestContext(request))

    return render_to_response('checkout/thanks.html', {
        'order': order,
        'message': message
    }, context_instance=RequestContext(request))

