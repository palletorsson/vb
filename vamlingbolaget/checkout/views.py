from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
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
            #print new_order.id
            new_order.ip = request.META['REMOTE_ADDR']
            new_order.status = 'O'

            c_items =  {}
            msg = "Order:\n"
            i = 1
            for item in cartitems:
                msg = msg + '# ' + str(i) + ': \n'
                msg = msg + 'Artikel : ' + item.article.name + ' (' + item.article.sku_number + ') \n'
                msg = msg + 'Monster : ' + item.pattern.name + ', Farg : ' + item.color.name + ' \n'
                msg = msg + 'Antal : ' + str(item.quantity) + ', Pris : ' + str(item.article.price) +  '\n'
                i = i + 1

            new_order.order_number = random.randrange(0, 111111, 3)
            msg = msg + 'Totalpris med handling : ' + str(totalprice)
            new_order.session_key = _cart_id(request)
            new_order.order = msg
            new_order.save()
            #from django.core.mail import send_mail

            #send_mail(subject, message, sender, recipients)
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
        message = "skicka en order"
        return render_to_response('checkout/thanks.html', {
            'message': message
        }, context_instance=RequestContext(request))

    return render_to_response('checkout/thanks.html', {
        'order': order,
        'message': message
    }, context_instance=RequestContext(request))

