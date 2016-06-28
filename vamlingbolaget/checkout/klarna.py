# -*- coding: UTF-8 -*-
'''Create example

This file demonstrates the use of the Klarna library to create an order.
'''
# Copyright 2015 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import klarnacheckout
from products.models import Color, Pattern, Size
from logger.views import keepLog


def get_connector(): 
    shared_secret = ''
    connector = klarnacheckout.create_connector(shared_secret,
                                            klarnacheckout.BASE_TEST_URL)
    return connector

def get_orderNone(): 
    return None

def get_merchant_urls(): 
    eid = '6460'
    merchant_url = "http://127.0.0.1:8000" # http://www.vamlingbolaget.com
    merchant = {
        'id': eid,
        'terms_uri': merchant_url + '/paymentterms',
        'checkout_uri': merchant_url + '/checkout/klarna',
        # add {checkout.order.id})
        'confirmation_uri': merchant_url + '/checkout/klhanks/',

        # You can not receive push notification on
        # a non publicly available uri
        # add  + {checkout.order.id})
        'push_uri': merchant_url +'/checkout/push_klar/{checkout.order.id}'
    }

    return merchant

def get_data_defaults(items): 
    merchant = get_merchant_urls()

    data = {
        'purchase_country': 'SE',
        'purchase_currency': 'SEK',
        'locale': 'sv-se',
        'merchant': merchant,
        'cart': { 
            'items': items
        }
    }
    return data

# data['recurring'] = True

def KlarnaOrderbyId(request_payload, shared_secret): 

    auth = base64(hex(sha256 (request_payload + shared_secret)))
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/customers?email="+email,
            headers = headers,
        )
        response = r.content
        response_exist_json = json.loads(response)

        if (response_exist_json['MetaInformation']['@TotalResources'] > 0): 
            return response_exist_json['Customers'][0]['@url']
        else:  
            return False 
         
    except requests.exceptions.RequestException as e:
        return('HTTP Request failed') 

def get_order(data):
    order = None
    try:
        connector = get_connector()
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst 

    order = klarnacheckout.Order(connector)

    try:
        print data
        order.create(data)
        order.fetch()
        order_id = order['id']
        print('Order ID: %s' % order_id)
    except klarnacheckout.HTTPResponseException as e:
        print(e.json.get('http_status_message'))
        print(e.json.get('internal_message'))


    order.fetch()

    # I add the session here this migth be wrong
    session = {}
    # Store order id of checkout session
    session['klarna_order_id'] = order_id
    html = "<div>%s</div>" % (order["gui"]["snippet"])
    return_obj = {}
    return_obj['order_id'] = order_id 
    return_obj['html'] = html
    # Display checkout
    return return_obj

def klarna_cart(order_json):  
    # make the str a python object
    # order_json = json.loads(order_json)
    cartitems = order_json['cartitems'] 
    rea_items = order_json['rea_items']

    #return cartitems
    invoicerows = []

    try:
        for item in cartitems: 
            color = Color.objects.get(order=item.color)
            pattern = Pattern.objects.get(order=item.pattern)
            size = Size.objects.get(pk=item.size)
            obj = {
                "quantity": int(item.quantity),
                "reference": str(item.article.sku_number), 
                "name": unicode(item.article.name) + " " + unicode(size)  + " " + unicode(pattern) + " " + unicode(color),
                "unit_price": item.article.price * 100,
                "discount_rate": 0,
                "tax_rate": 2500
            }
            invoicerows.append(obj)
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst   


    try:
        for item in rea_items:   
            invoicerows.append({
                "quantity": 1,
                "reference": str(item.reaArticle.article.sku_number), 
                "name": "Rea: " + unicode(item.reaArticle.article.name) + " "  + unicode(item.reaArticle.size)  + " " + unicode(item.reaArticle.pattern) + " " + unicode(item.reaArticle.color),
                "unit_price": item.reaArticle.article.price * 100,
                "discount_rate": 0,
                "tax_rate": 2500
            })


    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst   

    invoicerows.append({
        "quantity": 1,
        "reference": str(2), 
        "name": unicode("Handling"),
        "unit_price": 8000,
        "discount_rate": 0,
        "tax_rate": 2500
    })
    return invoicerows

def confirm_order_with_klarna(order_id): 
    connector = get_connector()
    order = klarnacheckout.Order(connector, order_id) 

    try:
        order.fetch()
    except klarnacheckout.HTTPResponseException as e:
        print(e.json.get('http_status_message'))
        print(e.json.get('internal_message'))
        order['status'] = ''
        order['http_status'] = e.json.get('http_status_message')
        order['internal_message'] = e.json.get('internal_message')

    if order['status'] == "checkout_complete": 

        # At this point make sure the order is created in your system and send a
        # confirmation email to the customer

        update = {};
       
        update['status'] = 'created'
        
        order.update(update)
         
        log = 'Klarna order push made successfully, order status: ' + order['status']
        keepLog('', log, 'INFO', '', order_id) 
        return update['status']

    log = 'Klarna order push was made to checkout already complete, status: ' + order['status'] 
    keepLog('', log, 'WARN', '', order_id) 
 
    return order['status']

def confirm_order(klarna_id): 
    # Instance of the HTTP library that is being used in the server

    connector = get_connector()
    print connector
    
    order = klarnacheckout.Order(connector, klarna_id)
    print order 
    order.fetch()
    return_obj = {}
    return_obj["shipping_address"] = order["shipping_address"]
    return_obj["html"] = "<div>%s</div>" % (order["gui"]["snippet"])

    return_obj["billingadress"] = order["billing_address"]

    #del session['klarna_order_id']
    return return_obj


def get_testcart(): 
    cart_test = (
        {
            'quantity': 1,
            'reference': '123456789',
            'name': 'Klarna t-shirt',
            'unit_price': 12300,
            'discount_rate': 1000,
            'tax_rate': 2500
        }, {
            'quantity': 1,
            'type': 'shipping_fee',
            'reference': 'SHIPPING',
            'name': 'Shipping Fee',
            'unit_price': 4900,
            'tax_rate': 2500
        }
    )
    return cart_test
