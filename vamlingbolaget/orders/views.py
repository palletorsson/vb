#-*-coding:utf-8-*-
from django.shortcuts import render
from checkout.models import Checkout
from products.models import Article, ReaArticle
from cart.views import getnames,totalsum
from models import OrderItem, ReaOrderItem
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from fortnox.fortnox import create_invoice_rows, searchCustomer, get_headers, createOrder
from django.http import HttpResponseRedirect
import json
from logger.views import keepLog
import requests
from requests.auth import HTTPDigestAuth
import json
#from checkout.views import fortnoxOrderandCostumer
import base64
from vamlingbolaget.settings import ROOT_DIR
import datetime

def CheckoutTransfer(checkout, cartitem, reaitems):

    if (cartitem):
        for item in cartitem:
            orderitem = OrderItem(checkout=checkout, article=item.article, color=item.color, color_2=item.color_2, pattern=item.pattern, pattern_2=item.pattern_2, size=item.size, date_added=item.date_added, quantity=item.quantity)
            orderitem.save()
    if (reaitems):  
        for item in reaitems:
            reaorderitem = ReaOrderItem(checkout=checkout, reaArticle=item.reaArticle, date_added=item.date_added)
            reaorderitem.save()    

    log = "Tranfer made from cart to order"
    keepLog('', log, 'INFO', '', checkout.order_number) 

    return True


 
def ShowOrders(request, stage='all'):
	if request.user.is_authenticated:
	    if stage == 'all': 
	        checkouts = Checkout.objects.filter(~Q(status='C')).exclude(status='F').order_by('-id')[:100]
	    elif stage == 'ordered':
	         checkouts = Checkout.objects.filter(status='O').order_by('-id')[:50]
	    elif stage == 'making':
	         checkouts = Checkout.objects.filter(status='M').order_by('-id')[:50]
	    elif stage == 'handling':
	         checkouts = Checkout.objects.filter(status='H').order_by('-id')[:50]
	    elif stage == 'shipped':
	         checkouts = Checkout.objects.filter(status='S').order_by('-id')[:50]
	    else: 
	    	 checkouts = Checkout.objects.filter(status='F').order_by('-id')[:50]

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
            secondmessage = u'Hej! \n\nVi på Vamlingbolaget vill återigen tack för din order. Din ordernummer är: 37827359723\nNu har vi in lagt din order för production. En order till Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg. \nSå fort det är klar kommer vi att skicka dina produkter. Då får du också ett nummer så du kan följa din order när den skickas. \n\nVänliga Hälsningar \nVamlingbolaget.'
        
        incolor_path = None
        fortnox = None
        if checkout.status == 'M': 
            allitems = {'cartitems': cartis, 'bargains': {}, 'voucher': {}, 'rea_items': reaitems}
            invoice_rows = create_invoice_rows(allitems)
            file_name = checkout.order_number
            incolor_path = '../../media/'+str(file_name)+'.txt'
            fortnox = 'Preview the order and customer information for the Fortnox invoice'
        
        unifaun = None
        pdf = checkout.unifaun_obj
        if checkout.status == 'H': 
            unifaun = u'Hej! \n\nNu är din order klar och skall skicka. \nFölj ditt paket här: 010102492148709. \nVänligen \nVamlingbolaget'

        lastmessage = None 
        if checkout.status == 'S': 
            lastmessage = u'Hej! \n\nFölj ditt paket här: 010102492148709. Innehållet: \nVänligen \nVamlingbolaget'
        
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
            'lastmessage': lastmessage
            },
            context_instance=RequestContext(request))

def loadShipment(request, id): 

    shipment = getShipment(id)
    
    return render_to_response('orders/shipment.html', {
        'shipment': shipment,
      
        },
        context_instance=RequestContext(request))

def OrderAction(request, todo, stage, order_number, send_type=''): 

    if request.user.is_authenticated:
        current_user = request.user
        order = Checkout.objects.filter(order_number=order_number)[0]

        if (stage == 'production'): 
            if todo == 'activate': 
                order.status = 'M'
                if order.paymentmethod == 'K': 
                    klarna_id = order.payex_key
                    requestKlarna(klarna_id)
                try:
                    makeLeaf(order)
                except: 
                    pass
                # send second email 
                #log process
                log = 'Order: ' + str(order.order_number) + ', Second email sent to: ' + order.email 
                keepLog(request, log, 'INFO', current_user, order.order_number) 


        if (stage == 'packaging'): 

            if todo == 'activate': 
                order.status = 'H'	
                # make Fortnox invoice
                new_order = order.order
                if len(order.fortnox_obj) < 100:
                    headers = get_headers()
                    resp = createOrder(headers, new_order)
                    order.fortnox_obj = resp
                    order.save()

                    #log process
                    if len(resp) < 100: 
                        log = 'Order: ' + str(order.order_number) + ', Fortnox order could not be created, view details'  
                        keepLog(request, log, 'WARN', current_user, order.order_number, resp)
                    else:  
                        log = 'Order: ' + str(order.order_number) + ', Fortnox order created, view details'  
                        keepLog(request, log, 'INFO', current_user, order.order_number, resp) 
                else:
                    log = 'Order: ' + str(order.order_number) + ', Fortnox order already created, view details'  
                    keepLog(request, log, 'WARN', current_user, order.order_number, order.fortnox_obj)


        if (stage == 'shipping'): 
            if todo == 'activate': 
                order.status = 'S'
                # make the Unifaun order 
                name = order.first_name +' '+ order.last_name
                #unifaunShipmentCall()
                receiver = getReceiver(name, order.email, order.street, order.postcode, order.city, order.country, order.phone)
                order_json = order.order
                if len(order_json) > 100:
                    parcel_json_len = 'long'
                else: 
                    parcel_json_len = 'short' 
                parcels = getParcels(order_json, parcel_json_len)
                pdfConf = getPdfConfig()
                service = getService(send_type)
                vamlingbolaget = getSender()
                opt =  getOptions(order.email)
                senderpartner = senderPartner(send_type)
                #checkZip(order.postcode)
                unifaunObj = {
                "pdfConfig": pdfConf,
                "shipment": {
                    "sender": vamlingbolaget,
                    "parcels": parcels,
                    "orderNo": str(order.order_number),
                    "receiver": receiver,
                    "service": service,
                    "senderReference": "Vamlingbolaget", 
				    "senderPartners": senderpartner,
                    "options": opt,
                    "test": "true"
 

                    }
                }
                shipmentparams = json.dumps(unifaunObj)


                shipment = unifaunShipmentCall(shipmentparams) 
                if len(shipment) < 100:
                    log = 'Order: ' + str(shipment) + ', Unifaun order creation error'
                    keepLog(request, log, 'ERROR', current_user, shipment) 
                else:
                    shipment_obj = json.loads(shipment)

                    pdf_href = shipment_obj[0]['pdfs'][0]['href']
                    shipment_id = shipment_obj[0]['id']
                    pdf = unifaunShipmentGetPDF(pdf_href, shipment_id)
                    order.unifaun_obj = pdf
                    order.save()
                    #log process
                    log = 'Order: ' + str(order.order_number) + ', Unifaun print created'
                    keepLog(request, log, 'INFO', current_user, order.order_number, pdf) 

        if (stage == 'finalize'): 
            order.status = 'F'
            # send shipping information to customer 
            # log process

            removeShipment('15977071')
            getShipmentsByDate('20160623')
            log = 'Order: ' + str(order.order_number) + ', Order Finlized '  
            keepLog(request, log, 'INFO', current_user, order.order_number, '')

        if stage == 'cancel':
            if todo == 'cancel':
                order.status = 'C'    	
                #log process
                log = 'Order: ' + str(order.order_number) + ', Order was cancelled'
                keepLog(request, log, 'INFO', current_user, order.order_number) 
        order.save()


        
        return HttpResponseRedirect('/orders/order/'+order_number)

def GetSecrets(): 
	return {'id': 'id', 'pass': 'pass'}

def GetHeaders():
    secrets = GetSecrets()
    encoded = base64.b64encode(secrets['id']+':'+secrets['pass'])
    basic_encoded = 'Basic '+encoded
    headers = {'Authorization': basic_encoded, 'Content-Type': 'application/json; charset=UTF-8'}
    return headers

def unifaunShipmentCall(shipmentparams):
    url = 'https://api.unifaun.com/rs-extapi/v1/shipments' 
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
    print r
    return r.content

def getShipment(id): 
    url = 'https://www.unifaunonline.se/rs-extapi/v1/shipments/'
    headers = GetHeaders() 
    r = requests.get(
            url, 
            headers=headers
            )
    print r
    print r.contentsq
    return r.content

def removeShipment(id): 
    url = 'https://www.unifaunonline.se/rs-extapi/v1/stored-shipments/'+id
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
    print sender_type 
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



def getParcels(parcel_json, parcel_json_len):
    weight = 0
    if parcel_json_len == 'long':
        return_parcels = []
        parcel_json = json.loads(parcel_json)
        parcel_json = parcel_json["Invoice"]["InvoiceRows"]
        
        for item in parcel_json: 
            if len(parcel_json) == 2:
                
                return_parcels = [{
                    "copies": "1",
                    "weight": "1",
                    "contents": item[0]["Description"]
                }]
                weight = weight + 0.5
            
    else:
        return_parcels = [{
      "copies": "1",
      "weight": str(weight),
      "contents": "Vamlingbolaget kläder",
    }]

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
                }],
        }
    else: 
        return {
          "id": service
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
      "city": city
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
        
        firstorder = firsTorder['Invoice']['YourOrderNumber']
        first_order_exist = True
        check_string = '["1":"OK"]'
    except:
        first_order_exist = False
        check_string = '["1":"NA"]'


    try: 
        fortnoXobj = json.loads(checkout.fortnox_obj) 
        orderNum = fortnoXobj['Invoice']['YourOrderNumber']
        order_exist = True 
        check_string = check_string + '["2":"OK"]'

    except:
        order_exist = False
        check_string = check_string + '["2":"NA"]'
       
    try: 
        unifaunMedia = checkout.unifaun_obj[:5] 

        if unifaunMedia == 'media': 
            shipping_exist = True 
            check_string = check_string + '["3":"OK"]'
    except:
        shipping_exist = False
        check_string = check_string + '["3":"NA"]'

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
        f.write('ORDER NR: ' + str(checkout.order_number)  + '\n' )
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