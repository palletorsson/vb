#-*-coding:utf-8-*-
from django.shortcuts import render
from checkout.models import Checkout
from checkout.views import fortnoxOrderandCostumer
from checkout.make_messages import email_two
from products.models import Article, ReaArticle
from cart.views import getnames,totalsum
from models import OrderItem, ReaOrderItem
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from fortnox.fortnox import create_invoice_rows, searchCustomer, get_headers, createOrder, get_stockvalue, get_articles, create_order_rows, InvoicefromOrder, create_invoice_rows, customerExistOrCreate, formatJson
from cart.views import getsize
from fortnox.fortnox import get_headers
from django.http import HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from logger.views import keepLog
import requests
from requests.auth import HTTPDigestAuth
import json
#from checkout.views import fortnoxOrderandCostumer
import base64
from vamlingbolaget.settings import ROOT_DIR
import datetime
import re
from django.core.mail import send_mail
from django.core import mail

def ShowOrders(request, stage='all'):
    if request.user.is_authenticated:
        if stage == 'all': 
            checkouts = Checkout.objects.filter(~Q(status='C')).exclude(status='F').order_by('-id')[:100]
        elif stage == 'ordered' or stage == 'card':
            checkouts = Checkout.objects.filter(status='O').order_by('-id')[:50]
        elif stage == 'making':
            checkouts = Checkout.objects.filter(status='M').order_by('-id')[:50]
        elif stage == 'handling':
            checkouts = Checkout.objects.filter(status='H').order_by('-id')[:50]
        elif stage == 'shipped':
            checkouts = Checkout.objects.filter(status='S').order_by('-id')[:50]
        else: 
            checkouts = Checkout.objects.filter(status='F').order_by('-id')[:50]

        for checkout in checkouts: 

            if len(checkout.fortnox_obj) > 200:
                checkout.fortnoxed = 1
            else: 
                checkout.fortnoxed = 0

        return render_to_response('orders/orders.html', {
	        'checkouts': checkouts,
	        },
	        context_instance=RequestContext(request))


 
def ShowOrder(request, order_id): 
    if request.user.is_authenticated:
        headers = get_headers()
        name = ''
        try: 
            checkout = Checkout.objects.filter(order_number=order_id)[0]
        except: 
            return HttpResponseRedirect('/orders/')
        process_status = LookAtDict(checkout)
        email = checkout.email
        cartis = checkout.orderitem_set.all()
        cartitems = checkout.orderitem_set.all()
        searchCustomer(headers, name, email)
        getnames(cartitems)
        stock = getOrderStock(cartitems)
        reaitems = checkout.reaorderitem_set.all()
        bargains = {}
        voucher = {}
        returntotal = totalsum(cartitems, bargains, request, voucher, reaitems)
        totalprice = returntotal['totalprice']
        handling = returntotal['handling']
        
        # check if customer exist in fortnox 
        fortnox_custumer = searchCustomer(headers, name, email=email)
        if fortnox_custumer == False:
            customer_number = 'New Customer'
        else:
            customer_number = fortnox_custumer.rsplit('/', 1)[-1]

        secondmessage = None
        if checkout.status == 'O': 
            secondmessage = email_two(request, checkout)
            # check if order exist in fortnox

        incolor_path = None
        fortnox = None
        if checkout.status == 'M': 
            allitems = {'cartitems': cartis, 'bargains': {}, 'voucher': {}, 'rea_items': reaitems}
            invoice_rows = create_order_rows(allitems)
            file_name = checkout.order_number
            incolor_path = '../../media/'+str(file_name)+'.txt'
            fortnox = 'Preview the order and customer information for the Fortnox invoice. The order will be added to Fortnox.'
        
        unifaun = None
        pdf = checkout.unifaun_obj
        if checkout.status == 'H': 
            unifaun = u'Hej! \n\nNu är din order klar och skall skicka. \nFölj ditt paket här: 010102492148709. \nVänligen \nVamlingbolaget'

        lastmessage = None 
        if checkout.status == 'S': 
            lastmessage = u'You can print the Shipping docs now or login to Unifaun later.  \nWhen you activate the postal docs in Unifaun an email will be send to the customer with shipment detail and tracking information.'
        
        return render_to_response('orders/order.html', {
            'order': checkout,
            'process_status': process_status,
            'cartitems':cartitems,
            'reaitems':reaitems,        
            'fortnox':fortnox,
            'incolor_path': incolor_path,  
            'secondmessage':  secondmessage, 
            'totalprice':totalprice,
            'handling':handling,
            'customer_number': customer_number,
            'unifaun': unifaun,
            'pdf':pdf, 
            'lastmessage': lastmessage,
            'stock': stock
            },
            context_instance=RequestContext(request))

def loadShipment(request, id=''): 

    shipment =  getShipments()
    
    return render_to_response('orders/shipment.html', {
        'shipment': shipment,
      
        },
        context_instance=RequestContext(request))


def loadShipments(request, id=''): 

    shipment =  getShipments()
    
    return render_to_response('orders/shipment.html', {
        'shipment': shipment,
      
        },
        context_instance=RequestContext(request))

def OrderAction(request, todo, stage, order_number, send_type=''): 

    if request.user.is_authenticated:
        current_user = request.user
        checkout = Checkout.objects.filter(order_number=order_number)[0]
        new_order_json = checkout.order
        what = 'order_json_done'
        if (stage == 'production'): 
            if todo == 'activate': 
                checkout.status = 'M'
                if checkout.paymentmethod == 'K': 
                    klarna_id = checkout.payex_key
                    requestKlarna(klarna_id)
                try:
                    makeLeaf(checkout)
                except: 
                    pass
                # send second email 
                secondmessage = email_two(request, checkout)
                to = [checkout.email, 'palle.torsson@gmail.com']
                #mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %secondmessage, checkout.email, to,  fail_silently=False)
                
                #log process
                log = 'Order: ' + str(checkout.order_number) + ', Second email sent to: ' + checkout.email 
                keepLog(request, log, 'INFO', current_user, checkout.order_number) 

        # init fortnox
        if (stage == 'packaging'): 

            if todo == 'activate': 
                checkout.status = 'H'
                headers = get_headers()	
                # load invoice
                what = 'order_json_done'
                if what == 'order_json_done':    
                    invoice_result = fortnoxOrderandCostumer(request, checkout, checkout.order, what)  
                    checkout.unifaun_obj = invoice_result                   
                    resp = createOrder(headers, invoice_result)
                    log = ' fortnox view details'  
                    keepLog(request, log, 'INFO', current_user, checkout.order_number, resp)
                    checkout.fortnox_obj = resp
                    checkout.save()       
                #log process
                if len(resp) < 100: 
                    log = 'Order: ' + str(checkout.order_number) + ', Fortnox order could not be created, view details'  
                    keepLog(request, log, 'WARN', current_user, checkout.order_number, resp)
                else:  
                    log = 'Order: ' + str(checkout.order_number) + ', Fortnox order created, view details'  
                    keepLog(request, log, 'INFO', current_user, checkout.order_number, resp) 
                
                   
        if (stage == 'shipping'): 
            if todo == 'activate': 
                checkout.status = 'S'
                # make the Unifaun order 
                name = checkout.first_name +' '+ checkout.last_name
                #unifaunShipmentCall()
                receiver = getReceiver(name, checkout.email, checkout.street, checkout.postcode, checkout.city, checkout.country, checkout.phone)
                checkout_json = checkout.order
                parcels = getParcels(checkout.fortnox_obj)
                pdfConf = getPdfConfig()
                service = getService(send_type)
                vamlingbolaget = getSender()
                opt =  getOptions(checkout.email)
                senderpartner = senderPartner(send_type)
                #checkZip(order.postcode)
                printing = 0
                if printing == 1: 
                    unifaunObj = {
                    "pdfConfig": pdfConf,
                    "shipment": {
                        "sender": vamlingbolaget,
                        "parcels": parcels,
                        "orderNo": str(checkout.order_number),
                        "receiver": receiver,
                        "service": service,
                        "senderReference": "Vamlingbolaget", 
    				    "senderPartners": senderpartner,
                        "options": opt, 
                        "test": True               
                        }
                    }
                else: 
                    unifaunObj = {
                        "sender": vamlingbolaget,
                        "parcels": parcels,
                        "orderNo": str(checkout.order_number),
                        "receiver": receiver,
                        "service": service,
                        "senderReference": "Vamlingbolaget", 
                        "senderPartners": senderpartner,
                        "options": opt,
                        "test": True,                 
                    }


                shipmentparams = json.dumps(unifaunObj)

                shipment = unifaunShipmentStoredCall(shipmentparams) 
                shipment_obj = json.loads(shipment)
                shipment_id = shipment_obj['id']
                checkout.unifaun_obj = shipment_id
                checkout.save()
                
                if len(shipment) < 100:
                    log = 'Order: ' + str(shipment) + ', Unifaun order creation error'
                    keepLog(request, log, 'ERROR', current_user, shipment) 
                else:

                    if printing == 1: 
                        shipment_obj = json.loads(shipment)

                        pdf_href = shipment_obj[0]['pdfs'][0]['href']
                        shipment_id = shipment_obj[0]['id']
                        pdf = unifaunShipmentGetPDF(pdf_href, shipment_id)
                        checkout.unifaun_obj = shipment_id
                        checkout.save()
                        #log process
                        log = 'checkout: ' + str(checkout.order_number) + ', Unifaun print created'
                        keepLog(request, log, 'INFO', current_user, checkout.order_number, pdf) 
                    else: 
                        print "no print"

        if (stage == 'finalize'): 
            checkout.status = 'F'
            # send shipping information to customer 
            # log process

            removeShipment('15977071')
            getShipmentsByDate('20160623')
            log = 'checkout: ' + str(checkout.order_number) + ', Order Finlized '  
            keepLog(request, log, 'INFO', current_user, checkout.order_number, '')

        if todo == 'cancel':
            if stage == 'cancel':
                checkout.status = 'C'    	
                #log process
                log = 'Order: ' + str(checkout.order_number) + ', Order was cancelled'
                keepLog(request, log, 'INFO', current_user, checkout.order_number) 

            if stage == 'shipment': 
                shipment_id = checkout.unifaun_obj 
                remove = removeShipment(shipment_id)
        checkout.save()


        
        return HttpResponseRedirect('/orders/order/'+order_number)

def GetSecrets(): 
	return {'id': 'id', 'pass': 'pass'}

def GetHeaders():
    secrets = GetSecrets()
    encoded = base64.b64encode(secrets['id']+':'+secrets['pass'])
    basic_encoded = 'Basic '+encoded
    headers = {'Authorization': basic_encoded, 'Content-Type': 'application/json; charset=UTF-8'}
    return headers

def getOrderStock(cartitems):
    for item in cartitems: 
        try: 
            size = item.size.pk
        except:  
            size = getsizenumber(item.size)
            
        fortnox_id = str(item.article.sku_number) + "_" + str(item.pattern.order) + "_" + str(item.color.order) + "_" + str(size)

        in_stock = get_stockvalue(fortnox_id)
        return in_stock
        

def getsizenumber(size):
    if size == 'XS': 
        return_size = 34 
    elif size == 'S': 
        return_size = 36
    elif size == 'M': 
        return_size = 3840
    elif size == 'L': 
        return_size = 42
    elif size == 'XL': 
        return_size =   44
    elif size == 'XXL':
        return_size = 46
    else: 
        return_size = 'NO' 

    return return_size

def unifaunShipmentCall(shipmentparams):
    url = 'https://api.unifaun.com/rs-extapi/v1/shipments' 
    headers = GetHeaders() 
    
    r = requests.post(
    			url, 
    			headers=headers, 
    			data=shipmentparams, 
    			)
    return r.content


def unifaunShipmentStoredCall(shipmentparams):
    url = 'https://api.unifaun.com/rs-extapi/v1/stored-shipments' 
    headers = GetHeaders() 
    
    r = requests.post(
                url, 
                headers=headers, 
                data=shipmentparams, 
                )
    return r.content

# https://www.unifaunonline.se/ufoweb-prod-201606211020/rs-extapi/v1/stored-shipments
# ?dateType=created&searchField=orderNo&searchOp=equals&status=ready

def getAllShipment(): 
    url = 'https://www.unifaunonline.se/rs-extapi/v1/stored-shipments/'
    headers = GetHeaders() 
    r = requests.get(
            url, 
            headers=headers
            )
    return r.content

def getShipments(): 
    url = 'https://www.unifaunonline.se/rs-extapi/v1/shipments/'
    headers = GetHeaders() 
    r = requests.get(
            url, 
            headers=headers
            )
    return True

def getShipment(id): 
    url = 'https://www.unifaunonline.se/rs-extapi/v1/shipments/'
    headers = GetHeaders() 
    r = requests.get(
            url, 
            headers=headers
            )
    return r.content


def removeShipment(id): 
    url = 'https://www.unifaunonline.se/rs-extapi/v1/shipments/'+id
    headers = GetHeaders() 
    r = requests.delete(
            url, 
            headers=headers
            )
    return r.content

def getShipmentsByDate(date):
    url = 'https://www.unifaunonline.se/rs-extapi/v1/stored-shipments?&dateType=created'
    headers = GetHeaders() 
    r = requests.get(
                url, 
                headers=headers
                )
    return r.content


def checkZip(zip):
    url = 'https://www.unifaunonline.se/rs-extapi/v1/addresses/zipcodes?countryCode=SE&zip='+zip
    headers = GetHeaders() 
    r = requests.get(
                url, 
                headers=headers
                )
    return r.content


def requestKlarna(klarna_id): 
    url =  'http://127.0.0.1:8000/checkout/push_klar/'+str(klarna_id)
    resp = requests.get(url)
    return resp.content
    
def unifaunShipmentGetPDF(href, id):
    url = href
    headers = GetHeaders()
    resp = requests.get(url, headers=headers)
    pdf_str = ROOT_DIR+'/media/'+id+'.pdf'
    with open(pdf_str, 'wb') as f:
        f.write(resp.content)
    return 'media/'+id+'.pdf'


def getShipmentPara():
    null = 'null'
    json = '{ "pdfConfig": { "target4XOffset": 0, "target2YOffset": 0, "target1Media": "laser-ste", "target1YOffset": 0, "target3YOffset": 0, "target2Media": "laser-a4", "target4YOffset": 0, "target4Media": null, "target3XOffset": 0, "target3Media": null, "target1XOffset": 0, "target2XOffset": 0 }, "shipment": { "sender": { "phone": "+46 31 725 35 00", "email": "info@unifaun.com", "quickId": "1", "zipcode": "41121", "name": "Unifaun AB", "address1": "Skeppsbron 5-6", "country": "SE", "city": "GÖTEBORG" }, "parcels": [{ "copies": "1", "weight": "2.75", "contents": "important things", "valuePerParcel": true }], "orderNo": "order number 123", "receiver": { "phone": "+46 8 34 35 15", "email": "sales@unifaun.com", "zipcode": "11359", "name": "Unifaun AB", "address1": "Tegnérgatan 34", "country": "SE", "city": "STOCKHOLM" }, "senderReference": "sender ref 234", "service": { "id": "P15" }, "receiverReference": "receiver ref 345", "options": [{ "message": "This is order number 123", "to": "sales@unifaun.com", "id": "ENOT", "languageCode": "SE", "from": "info@unifaun.com" }] } }'
    json2 = '{"pdfConfig": {"target4YOffset": 0, "target2XOffset": 0, "target2YOffset": 0, "target4XOffset": 0, "target2Media": "laser-a4", "target1XOffset": 0, "target1Media": "laser-ste", "target3XOffset": 0, "target3YOffset": 0, "target3Media": "null", "target1YOffset": 0, "target4Media": "null"}, "shipment": {"options": [{"to": "sales@unifaun.com", "message": "This is order number 123", "from": "info@unifaun.com", "id": "ENOT", "languageCode": "SE"}], "Party_CustNo": {"location":"Stockholm"},"senderPartners": [{ "id": "001", "custNo": "001" }], "sender": {"phone": "+46 31 725 35 00", "city": "G\u00d6TEBORG", "name": "Unifaun AB", "address1": "Skeppsbron 5-6", "quickId": "1", "country": "SE", "email": "info@unifaun.com", "zipcode": "41121"}, "service": {"id": "P15"}, "receiver": {"city": "STOCKHOLM", "name": "Unifaun AB", "address1": "Tegn\u00e9rgatan 34", "zipcode": "11359", "phone": "+46 8 34 35 15", "country": "SE", "email": "sales@unifaun.com"}, "orderNo": "order number 123", "receiverReference": "receiver ref 345", "parcels": [{"contents": "important things", "copies": "1", "weight": "2.75", "location": "gotland"}], "senderReference": "sender ref 234"}}' 
    return json2

def senderPartner(sender_type):
    if sender_type == "PAF": 
        senderpartner = "PBREV" 
        custno = "011111118"
    if sender_type == "P15": 
        senderpartner = "PLAB" 
        custno = "0111111118"
    if sender_type == "PUA":
        senderpartner = "PBREV" 
        custno = "01111118" 

    return [{ "id": senderpartner,
        "custNo": custno }]



def getParcels(parcel_json):
    weight = 0

    return_parcels = []
    parcel_json = json.loads(parcel_json)

    parcel_json = parcel_json["Invoice"]["InvoiceRows"]
    for item in parcel_json: 
        try: 
            art_num = item['ArticleNumber']
            artnum = re.sub(r'[\W_]+', '', art_num)
            artnum = int(artnum)

            if artnum > 10: 
                
                return_parcels.append({
                    "copies": "1",
                    "weight": "1",
                    "contents": item['Description']
                })
                weight = weight + 0.5
        except: 
            pass     

    return return_parcels 

def getPdfConfig(): 
    return {
    "target4XOffset": 0,
    "target2YOffset": 0,
    "target1Media": "laser-a4",
    "target1YOffset": 0,
    "target3YOffset": 0,
    "target2Media": "laser-ste",
    "target4YOffset": 0,
    "target4Media": 0,
    "target3XOffset": 0,
    "target3Media": 0,
    "target1XOffset": 0,
    "target2XOffset": 0
    }

# "id": "P15"
def getService(service):
    if service == "PAF": 
        return {
          "id": service,
          "paymentMethodType": "invodn",  
           "addons": [{
                 "id": "PAF"
                },
                {
                "id": "COD",
                "amount": 100
                },
                { 
                "id": "NOT"
                }
                ],
        }
    else: 
        return {
          "id": service, 
          "addons": [{
            "id": "NOT"
            }]
        }
        

def getSender(): 
    return {
	  "phone": "+46 498 49 80 80",
	  "email": "info@vamlingbolaget.com",
	  "quickId": "1",
	  "zipcode": "62331",
	  "name": "Vamlingbolaget Gotland AB",
	  "address1": "Vamlingbo Ängvards 302",
	  "country": "SE",
	  "city": "Burgsvik"
	}


def getReceiver(name, email, adress1, zipcode, city, country, phone): 
    return {
      "phone": phone,
      "email": email,
      "zipcode": zipcode,
      "name": name,
      "address1": adress1,
      "country": "SE",
      "city": city,
     
    }


def getOptions(email): 
    return {
      "message": "Vamlingbolaget har skickat din Order",
      "to": email,
      "id": "ENOT",
      "languageCode": "SE",
      "from": "info@vamlingbolaget.com"
    },
    {
      "id": "CONSOLIDATE",
      "sendEmail": true,
      "key": "testapi1"
    }

def LookAtDict(checkout):
    check_string = ''
    first_order_exist = False
    order_exist = False
    shipping_exist = False

    try: 
        firsTorder = json.loads(checkout.order) 
        
        firstorder = firsTorder['Invoice']['CustomerNumber']
        first_order_exist = True
        check_string = 'Order: <span class="glyphicon glyphicon-ok" aria-hidden="true"> </span> | '
    except:
        first_order_exist = False
        check_string = 'Order: <span class="glyphicon glyphicon-option-horizontal" aria-hidden="true"> </span> | '


    try: 
        fortnoXobj = json.loads(checkout.fortnox_obj) 

        orderNum = fortnoXobj['Invoice']['DocumentNumber']
        order_exist = True 
        check_string = check_string + 'Fortnox: <span class="glyphicon glyphicon-ok" aria-hidden="true"> </span> | '

    except:
        order_exist = False
        check_string = check_string + 'Fortnox: <span class="glyphicon glyphicon-option-horizontal" aria-hidden="true"> </span> | '
    
    # make a request to see if 

    try: 
        shipment_id = checkout.unifaun_obj
        if len(shipment_id) > 3: 
            shipping_exist = True 
            check_string = check_string + 'Unifaun: <span class="glyphicon glyphicon-ok" aria-hidden="true"> </span>'
        else: 

            shipping_exist = False
            check_string = check_string + 'Unifaun: <span class="glyphicon glyphicon-option-horizontal" aria-hidden="true"> </span> '    
    except:
        shipping_exist = False
        check_string = check_string + 'Unifaun: <span class="glyphicon glyphicon-option-horizontal" aria-hidden="true"> </span> '

    return check_string


def makeLeaf(checkout):
    cartitems = checkout.orderitem_set.all()
    headers = get_headers()
    searchCustomer(headers, '', checkout.email)
    getnames(cartitems)
    reaitems = checkout.reaorderitem_set.all()
    
    fortnox_custumer = searchCustomer(headers, '', email=checkout.email)
    

    file_name = checkout.order_number
    txt_path = ROOT_DIR+'/media/'+str(file_name)+'.txt'

    f = open(txt_path, 'w')

    for item in cartitems: 
        
        f.write('\n') 
        f.write("INFARGNINGSSEDEL -------- DATUM: " + str(datetime.date.today()) + '\n')
        f.write('-------------------------------------------\n')
        f.write('\n')
        f.write('KUND: ' + fortnox_custumer.rsplit('/', 1)[-1] + '  ---------------  ')
        f.write('ORDER NR: ' + str(checkout.order_number) + '\n' )
        f.write('-------------------------------------------\n')

        f.write('\n')
        f.write('ARTIKEL: \n')        
        f.write('-------------------------------------------\n')
        f.write('ART NR: '+ str(item.article.sku_number).encode('iso-8859-1') + '\n' )
        f.write('-------------------------------------------\n')
        f.write('PLAGG: '+  item.article.name.encode('iso-8859-1') + '\n' )
        f.write('-------------------------------------------\n')
        f.write('FARG: '+  str(item.color).encode('iso-8859-1') + ' -- ')
        f.write('MONSTER: '+  str(item.pattern).encode('iso-8859-1') + ' \n')
        if (item.pattern_2 != 0):
            f.write('FARG2: '+  str(item.color2).encode('iso-8859-1') + ' -- ')
            f.write('MONSTER2: '+  str(item.pattern2).encode('iso-8859-1') + ' \n')     
        f.write('-------------------------------------------\n')      

        f.write('ANTAL: '+ str(item.quantity) + '\n' )
        f.write('\n')
        f.write('KOMMENTAR:\n')  
        f.write('-------------------------------------------\n\n\n\n\n')  
        f.write('-------------------------------------------\n') 
        f.write('\n\n\n\n') 

    f.closed

    return 1

def getFornoxArticles(request, page): 
    headers = get_headers()
    articles = get_articles(headers, page)
    articles = json.loads(articles)
    articles = articles['Articles']
    r_articles = []

    for art in articles:
        temp = {}
        temp['Description'] = art['Description']
        temp['ArticleNumber'] = art['ArticleNumber']
        temp['QuantityInStock'] = art['QuantityInStock']
        temp['url'] = art['@url']
        
        r_articles.append(temp)

    return render_to_response('orders/articles.html', {
        'articles': r_articles,
        },
        context_instance=RequestContext(request))

@login_required
def getAllemail(request):
    checkouts = Checkout.objects.all()
    emaillist = []
    file = open('emails.txt', 'w+')
    
    for checkout in checkouts:
        if not checkout.email in emaillist:
            emaillist.append(checkout.email)
            file.write(checkout.email + ", ")

    return HttpResponse(status=200)

