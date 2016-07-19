from django import template
from django.templatetags.static import register
from cart.models import Cart
from cart.views import _cart_id, totalsum

register = template.Library()

#@register.tag(name='cart_total')
def cart_total(context):
    has_items = False
    request = context['request']
    key = _cart_id(request)
    cart, created = Cart.objects.get_or_create(key=key)
    cartitems = cart.cartitem_set.all()
    bargains = cart.bargaincartitem_set.all()
    voucher = cart.vouchercart_set.all()
    rea = cart.reacartitem_set.all()
    returntotal = totalsum(cartitems, bargains, request, voucher, rea)
    total = returntotal['totalprice']
    numbers = returntotal['totalitems']
    if numbers > 0: 
        has_items = True
    return { 'total': total, 'numbers': numbers, 'has_items': has_items }

register.inclusion_tag('cart/cart_template.html', takes_context = True)(cart_total)
