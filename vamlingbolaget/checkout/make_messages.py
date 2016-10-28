#-*-coding:utf-8-*-

from string import Template
from django.utils import translation
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from products.models import Pattern, Color
from fortnox.fortnox import getFortnoxSize

# start by creating the costumer message header 
def head_part_of_message(lang): 

    yourorderto = 'Din order till Vamlingbolaget'
    yourorder = 'Din order'

    if lang == 'en': 
        yourorderto = 'Your order to Vamlingbolaget'
        yourorder = 'Your order'

    s = Template('$yourorderto_ :, \n--------------------------------- \n$yourorder_ \n')
    message_header = s.substitute(yourorderto_=yourorderto, yourorder_=yourorder)
    return message_header

# continue to build the message cart summery
def cart_part_of_message(cartitems, rea_items, lang, i=1): 

    cartitems_str = ''

    product = 'Produkt'
    amount = 'st'
    itsin = 'i'
    outsida = 'utsida'
    insida = 'insida'
    itsand = 'och'
    size = 'Storlek'
    priceperproduct = "Pris per produkt"

    if lang == 'en': 
        product = 'Product'
        amount = ''
        itsin = 'in'
        outsida = 'outside'
        insida = 'inside'
        itsand = 'and'
        size = 'Size'
        priceperproduct = "Price per product"

    for item in cartitems:
        s = Template('----------- \n$product_ $num_ : \n$item_quantity $amount_ $art_name ( $art_sku ) \n')
        cart_temp = s.substitute(product_=product, num_=str(i), item_quantity=str(item.quantity), amount_=amount, art_name=item.article.name, art_sku=item.article.sku_number, )

        if (item.pattern_2 != 0):
            u = Template('$in_ $patternname, $patterncolor ( $outside_ )\n$and_ $patternname2 , $patterncolor2 ( $inside_ )\n')
            cart_temp = cart_temp + u.substitute(in_=itsin, patternname=item.pattern.name, patterncolor=item.color.name, outside_=outsida, and_=itsand, patternname2=item.pattern_2.name, patterncolor2=item.color_2.name, inside_=insida, ) 
        else:
            u = Template('$in_ $patternname, $patterncolor \n')
            cart_temp = cart_temp + u.substitute(in_=itsin, patternname=item.pattern.name, patterncolor=item.color.name, ) 

        if (item.article.type.order < 7 or item.article.type.order == 9):
            v = Template('$size_ : $size_name \n')
            try:
                cart_temp = cart_temp + v.substitute(size_=size, size_name=item.size.name,) 
            except:
                cart_temp = cart_temp + v.substitute(size_=size, size_name=item.size) 

        t = Template('$productprice_ : $price $sek_ \n')
        cart_temp = cart_temp + t.substitute(productprice_=priceperproduct, price=str(item.article.price), sek_='SEK') 

        cartitems_str = cartitems_str + cart_temp     
        i = i + 1

    for item in rea_items:   
        s = Template('----------- \n$product_ $num_ : (REA) \n$item_quantity $amount_ $art_name ( $art_sku ) \n')
        cart_temp = s.substitute(product_=product, num_=str(i), item_quantity=str(1), amount_=amount, art_name=item.reaArticle.article.name, art_sku=item.reaArticle.article.sku_number, )
        u = Template('$in_ $patternname, $patterncolor \n')
        cart_temp = cart_temp + u.substitute(in_=itsin, patternname=item.reaArticle.pattern.name, patterncolor=item.reaArticle.color.name, ) 
        v = Template('$size_ : $size_name \n')
        cart_temp = cart_temp + v.substitute(size_=size, size_name=item.reaArticle.size.name,) 
        t = Template('$productprice_ : $price $sek_  (REA) \n')
        cart_temp = cart_temp + t.substitute(productprice_=priceperproduct, price=str(item.reaArticle.rea_price), sek_='SEK') 

        cartitems_str = cartitems_str + cart_temp                   
                
    return cartitems_str

# continue to build summery of the message from form values
def cartsum_part_of_message(handling, totalprice, lang):

    transporthandling = 'Frakt och hantering'

    if lang == 'en': 
        transporthandling = 'Shipping and handling'


    # continue to build summery of the message from form values
    u = Template('---------------------------------\n$transporthandling_ : $handling SEK \n--------------------------------- \nSum ------------------- $totalprice_ SEK \n--------------------------------- \n')
    sum = u.substitute(transporthandling_=transporthandling, handling=handling, totalprice_=totalprice)
    return sum

# continue and add if costumer added personal message 
def personal_part_of_message(message, lang):
    yourmess = 'Ditt Meddelande till oss'

    if lang == 'en': 
        yourmess = 'Your Message to us'


    # continue to build summery of the message from form values
    u = Template('\n$yourmess_ : \n--------------------------------- \n$message \n--------------------------------- \n')
    mess = u.substitute(yourmess_=yourmess, message=message)
    return mess


def adress_part_of_message(new_order, lang): 

    youradress = 'Din adress'
    yourphone = 'Ditt telefonnummer'

    if lang == 'en': 
        youradress = 'Your address'
        yourphone = 'Your phone number'

    # build the adress part
    s = Template('\n$youradress_ :\n------------- \n$first_name $last_name \n$street \n$postcode $city \n$country \n--------------------------------- \n$yourphone_ : $phone \n')
    address_str = s.substitute(youradress_=youradress, first_name=new_order.first_name, last_name=new_order.last_name, street=new_order.street, postcode=new_order.postcode, city=new_order.city, country=new_order.country, yourphone_=yourphone, phone=new_order.phone)
    return address_str

# finalize the message     
def final_part_of_message(new_order, lang): 
    last_part_message = ''
    handling = 'En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. Reaplagg tar ca 1 vecka.'
    youpaypostal = 'Du betalar med postforskott'
    youpaypayex = 'Du valde Payex kortbetalning'
    youpayklarna = 'Du valde Klarna checkout'
    sms_notice = 'sms-avisering kommer'
    yourordernumber = 'Ditt ordernummer'

    if lang == 'en': 
        handling = 'An order to Vamlingbolaget takes about 3 weeks since we sew your garments. Rea items takes about 1 week. '
        youpaypostal = 'You pay cash on delivery '
        youpaypayex = 'You chose Payex card payments '
        youpayklarna = 'You chose Klarna checkout'
        sms_notice = 'You will receive an SMS notification'
        yourordernumber = 'Your order number is'

    s = Template('----------------------------------------------------------------------------------------------------------\n* $handling_ \n')
    last_part_message = last_part_message + s.substitute(handling_=handling, )

    # check it the method is to pay --> with card | on delivery  
    if (new_order.paymentmethod == 'P'):
        s = Template('* $youpaypostal_ \n')
        last_part_message = last_part_message + s.substitute(youpaypostal_=unicode(youpaypostal), )
    if (new_order.paymentmethod == 'C'):
        s = Template('* $youpaypayex_ \n')
        last_part_message = last_part_message + s.substitute(youpaypayex_=youpaypayex, )
    if (new_order.paymentmethod == 'K'):
        s = Template('* $youpayklarna_ \n')
        last_part_message = last_part_message + s.substitute(youpayklarna_=youpayklarna, )

    s = Template('* $sms_notice_ \n')
    last_part_message = last_part_message + s.substitute(sms_notice_=sms_notice, )

    s = Template('---------------------------------\n$yourordernumber_ : $ordernumber \n---------------------------------\n')
    last_part_message = last_part_message + s.substitute(yourordernumber_=yourordernumber, ordernumber=new_order.order_number, )

    return last_part_message


def getAllMessages(lang): 
    #
    yourorderto = 'Din order till Vamlingbolaget'
    yourorder = 'Din order'
    #
    product = 'Produkt'
    amount = 'st'
    itsin = 'i'
    outsida = 'utsida'
    insida = 'insida'
    itsand = 'och'
    size = 'Storlek'
    priceperproduct = "Pris per produkt"
    #
    transporthandling = 'Frakt och hantering'
    #
    youradress = 'Din adress'
    yourphone = 'Ditt telefonnummer'
    #
    last_part_message = ''
    handling = 'En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. Reaplagg tar ca 1 vecka.'
    youpaypostal = 'Du betalar med postforskott'
    youpaypayex = 'Du valde Payex kortbetalning'
    youpayklarna = 'Du valde Klarna checkout'
    sms_notice = 'sms-avisering kommer'
    yourordernumber = 'Ditt ordernummer'

    if lang == 'en': 
        #
        yourorderto = 'Your order to Vamlingbolaget'
        yourorder = 'Your order'
        #
        product = 'Product'
        amount = ''
        itsin = 'in'
        outsida = 'outside'
        insida = 'inside'
        itsand = 'and'
        size = 'Size'
        priceperproduct = "Price per product"
        #
        transporthandling = 'Shipping and handling'
        #
        youradress = 'Your address'
        yourphone = 'Your phone number'
        #
        handling = 'An order to Vamlingbolaget takes about 3 weeks if we sew your garments. Otherwise about a week. '
        youpaypostal = 'You pay cash on delivery '
        youpaypayex = 'You chose Payex card payments '
        youpayklarna = 'You chose Klarna checkout'
        sms_notice = 'You will receive an SMS notification'
        yourordernumber = 'Your order number is'



def email_one(request, new_order, cartitems, handling, totalprice):

    # get the name of color and patterns
    for item in cartitems:
        color = Color.objects.get(order=item.color)
        item.color_text = color.name
        pattern = Pattern.objects.get(order=item.pattern)
        item.pattern_text = pattern.name
        if (item.color_2):
            color = Color.objects.get(order=item.color_2)
            item.color_text_2 = color
            pattern = Pattern.objects.get(order=item.pattern_2)
            item.pattern_text_2 = pattern
        try:
            text_size = getFortnoxSize(item.size)
        except: 
            text_size = ''
        item.size_text = text_size

    # get the name of the size 
        

    ctx = {
        'handling' : handling,
        'totalprice' : totalprice,
        'cartitems' : cartitems,
        'new_order': new_order
    }

    # save the langage code
    lang = request.LANGUAGE_CODE 

    # Make messages
    message_en  = render_to_string('checkout/email_en.txt', ctx)

    # reset the language
    translation.activate(lang) 

    # return the right combiantion of message
    if lang == 'en': 
        message = message_en 
    elif lang == 'sv': 
        message_se = render_to_string('checkout/email_se.txt', ctx)
        message = message_se
    elif lang == 'fi':
        message_fi  = render_to_string('checkout/email_fi.txt', ctx) 
        message = message_fi + message_en
    elif lang == 'dk': 
        message_dk  = render_to_string('checkout/email_en.txt', ctx)
        message = message_dk + message_en
    elif lang == 'de': 
        message_de  = render_to_string('checkout/email_en.txt', ctx)
        message = message_de + message_en
    else: 
        message = message_en 
      
    return message 

def email_two(request, new_order):

    # get the name of color and patterns
    
    ctx = {
        'new_order': new_order
    }

    # save the langage code
    lang = request.LANGUAGE_CODE 

    # Make messages
    translation.activate('se')
    message_se = render_to_string('checkout/email2_se.txt', ctx)
    message_en = render_to_string('checkout/email2_se.txt', ctx)
    translation.activate(lang) 

    # return the right combiantion of message
    if lang == 'en': 
        message = message_en 
    elif lang == 'se': 
        message = message_se
    elif lang == 'fi': 
        message = message_fi + message_en
    elif lang == 'dk': 
        message = message_en + message_en
    elif lang == 'de': 
        message = message_en + message_en
    else: 
        message = message_en 
      
    return message 