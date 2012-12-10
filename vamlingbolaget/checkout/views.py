from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core import mail
from cart.views import _cart_id, totalsum, _new_cart_id

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
            first_name = str(request.POST['first_name'])
            last_name = str(request.POST['last_name'])
            street = request.POST['street']
            postcode = int(request.POST['postcode'])
            city = request.POST['city']
            if (request.POST['country']):
                country = request.POST['country']
            else:
                country = 'none'
            if (request.POST['message']):
                message = request.POST['message']
            else:
                message = 'none'

            msg = "> Din order till Vamlingbolaget:\n"
            msg = msg + '-------------------------------- *\n'
            msg = msg + '> Din adress ------------------------------------------------------------------------------------------ *\n'
            msg = msg + u'%s %s \n' % (first_name, last_name)
            msg = msg + u'%s \n' % (street)
            msg = msg + u'%d %s \n' % (postcode, city)
            if (country != 'none'):
                msg = msg + u'%s \n' % (country)
            i = 1
            msg = msg + '> Din order ------------------------------------------------------------------------------------------- *\n'
            for item in cartitems:
                msg = msg + 'plagg '+ str(i) + ': \n'
                msg = msg +  str(item.quantity) + ' st ' + item.article.name + ' (' + item.article.sku_number + ') '
                msg = msg + 'i ' + item.pattern.name + ', ' + item.color.name + ' \n'
                msg = msg + 'Pris per plagg: ' + str(item.article.price) +  ' SEK \n'
                i = i + 1
            msg = msg + '------------------------------------------------------------------------------------------------------- *\n'
            msg = msg + 'Frakt och Hantering: 50 SEK \n'
            msg = msg + '------------------------------------------------------------------------------------------------------- *\n'
            msg = msg + '> Totalpris: %s SEK \n' %str(totalprice)
            msg = msg + '------------------------------------------------------------------------------------------------------- *\n'
            msg = msg + '> En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. \n'
            msg = msg + '------------------------------------------------------------------------------------------------------- *\n'
            msg = msg + '> Du betalar med postforskatt \n'
            msg = msg + '------------------------------------------------------------------------------------------------------- *\n'
            if (message != 'none'):
                msg = msg + 'Din Meddelande ----------------------------------------------------------------------------------------- *\n'
                msg = msg + u' %s \n' % (message)
                msg = msg + '------------------------------------------------------------------------------------------------------- *\n'
            msg = msg + '> Tack!'
            new_order.order_number = random.randrange(0, 111111, 3)
            new_order.session_key = _cart_id(request)
            new_order.order = msg
            new_order.save()
            to = [request.POST['email'],]
            mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %msg, 'vamlingbolagetorder@gmail.com', to,  fail_silently=False)

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

