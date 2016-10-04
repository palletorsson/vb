import requests
import json
import requests
import httplib
from local_fortnox import get_headers
import csv
from products.models import *


local_tests = True; 

# Fortnox
# Value helper function
def get_art_temp(): 
    return "DE_782"

#testing
def get_testCustomer(): 
    customer = json.dumps({
            "Customer": {
                "Name": unicode("Rulle Torsson"),
                "Address1": unicode("Olkungag 72"),
                "City": unicode("Stockholm"),
                "ZipCode": unicode("12044"),
                "Email": unicode("smaskis@gmail.com"),
                "Phone1": unicode("0760890023"),
            }
        })
    return customer

# Functions

# Jsons
# Create a json-object from givendata for update
def json_update(articleNumber, QuantityInStock): 
    data_ = json.dumps({
                "Article": {
                    "QuantityInStock": QuantityInStock,
                    "ArticleNumber": articleNumber,			
                }
            })
    return data_

def create_invoice_rows(order_json):
    
    cartitems = order_json['cartitems'] 
    rea_items = order_json['rea_items']

    invoicerows = []

    for item in cartitems: 
        color = Color.objects.get(order=item.color)

        pattern = Pattern.objects.get(order=item.pattern)


        size = Size.objects.get(pk=item.size)

        obj = {
            "DeliveredQuantity": int(item.quantity),
            "ArticleNumber": int(item.article.sku_number), 
            "Description": unicode(item.article.name) + " " + unicode(size) 
        }

        invoicerows.append(obj)
        invoicerows.append({
            "Description": unicode(pattern) + " " + unicode(color) 
        })


    try:
        for item in rea_items:   
            invoicerows.append({
    	        "DeliveredQuantity": 1,
    	        "ArticleNumber": int(item.reaArticle.article.sku_number), 
    		    "Description": "Rea: " + unicode(item.reaArticle.article.name) + " "  + unicode(item.reaArticle.size),
                "Price": item.reaArticle.article.price,
                "Discount": 30,
                "DiscountType": "PERCENT"
    	    })
            invoicerows.append({
                "Description": unicode(item.reaArticle.pattern) + " " + unicode(item.reaArticle.color)
            })
    except:
        print "no reaitem"

    invoicerows.append({
        "DeliveredQuantity": 1,
        "ArticleNumber": 2, 
        "Description": "Postavgift"
     })

    return invoicerows  

def create_order_rows(order_json):
    print "order rows"
    cartitems = order_json['cartitems'] 
    rea_items = order_json['rea_items']

    invoicerows = []

    for item in cartitems: 
        full = False
        color = Color.objects.get(order=item.color)
        pattern = Pattern.objects.get(order=item.pattern)
        variation = Variation.objects.get(article=item.article, color=color, pattern=pattern)

        # use the try statment to check if it is a full varition  
        try: 
            full_var = FullVariation.objects.get(variation=variation, size=item.size)
            # create the full article number here
            full_var_num = str(full_var.variation.article.sku_number) + "_" + str(full_var.variation.pattern.order) + "_" + str(full_var.variation.color.order)  + "_" + str(full_var.size)
            full = True
        except:
            pass 

        if full == True: 
            # here we it could be good to do get the size        
            obj = {
                "OrderedQuantity": int(item.quantity),
                "ArticleNumber": full_var_num, 
                "Description": unicode(full_var) 
            }
            invoicerows.append(obj)
    
        if full == False: 
            size = Size.objects.get(pk=item.size)
            obj = {
                "OrderedQuantity": int(item.quantity),
                "ArticleNumber": int(item.article.sku_number), 
                "Description": unicode(item.article.name) + " " + unicode(size) 
            }
            invoicerows.append(obj)
            invoicerows.append({
                "Description": unicode(pattern) + " " + unicode(color) 
            })
    
    try:
        for item in rea_items:   
            invoicerows.append({
                "OrderedQuantity": 1,
                "ArticleNumber": int(item.reaArticle.article.sku_number), 
                "Description": "Rea: " + unicode(item.reaArticle.article.name) + " "  + unicode(item.reaArticle.size),
                "Price": item.reaArticle.article.price,
                "Discount": 30,
                "DiscountType": "PERCENT"
            })
            invoicerows.append({
                "Description": unicode(item.reaArticle.pattern) + " " + unicode(item.reaArticle.color)
            })
    except:
        print "no reaitem"

    invoicerows.append({
        "OrderedQuantity": 1,
        "ArticleNumber": 2, 
        "Description": "Postavgift"
    })

    return invoicerows   

# Interact with API

#https://api.fortnox.se/3/customers?email=palle.torsson@gmail.com
def searchCustomer(headers, name, email): 
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

#https://api.fortnox.se/3/customers?email=palle.torsson@gmail.com
def searchCustomerByEmail(headers, email): 
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

def extractCustmer(customer_meta): 
    customer_meta = json.loads(customer_meta)
    try: 
        customer_meta = customer_meta['Customers'][0]
    except: 
        pass 

    customer = json.dumps({
            "Customer": {
                "Name": unicode(customer_meta['Name']),
                "Address1": unicode(customer_meta['Address1']),
                "City": unicode(customer_meta['City']),
                "ZipCode": unicode(customer_meta['ZipCode']),
                "Email": unicode(customer_meta['Email']),
                "Phone1": unicode(customer_meta['Phone']),
            }
        })
    return customer 


# Create customer
def CreateCostumer(headers, customer): 

    isdict = type(customer) is dict 

    if (isdict): 
        print "is dict" 
    else:      
       customer = formatJson(customer)

    try:
        r = requests.post(
        url="https://api.fortnox.se/3/customers",
            headers = headers,
            data = customer
        )
    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')

    try:    
        result = json.loads(r.content)
    except: 
        result = r.content

    customer_response = result['Customer']['CustomerNumber']

    return customer_response

 
def formatCustomer(customer): 
    customer = json.dumps({
            "Customer": {
                customer
            }
        })
    return customer


# Update customer
def updateCostumer(headers, customer, customer_url):

    isdict = type(customer) is dict 
    if (isdict): 
        print "is dict" 
    else:      
       customer = formatJson(customer)
     
    try:
        r = requests.put(
            url=customer_url,
            headers = headers,
            data = customer
        )

    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')
    try:    
        result = json.loads(r.content)
    except: 
        result = r.content

    customer_response = result['Customer']['CustomerNumber']
        
    return customer_response

# Create or update customer
def customerExistOrCreate(headers, customer, order): 

    isdict = type(customer) is dict 
    if (isdict): 
        print "is dict"
    else:      
       customer = formatJson(customer)

    customer_dict = json.loads(customer)

    # see if custumer exist
    customer_exist = searchCustomer(headers, customer_dict['Customer']['Name'], customer_dict['Customer']['Email']) 
    print "searchCustomer" 
    print customer_exist

    if(customer_exist == False):
        try: 
            customer_response_id = CreateCostumer(headers, customer)
            print  "cust id new: " + str(customer_response_id)  
            return customer_response_id
        except: 
            customer_response = "Create error: " + str(customer_response)
       
    if(customer_exist != False):
        try:
            url = customer_exist
            #the returning result is customer id  
            customer_response_id = updateCostumer(headers, customer, url)
            print  "cost id old: " + str(customer_response_id)   
            return customer_response_id
        except: 
            customer_response = "Update error: " + str(customer_response)

    return customer_response

#look for order (invoice)

def getOrders(headers):
    # Invoices (GET https://api.fortnox.se/3/invoices)

    try:
        r = requests.get(
            url="https://api.fortnox.se/3/invoices",
            headers = headers,
        )
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
    return r.content


def seekOrder(headers, custumer_name):
    # Invoices (GET https://api.fortnox.se/3/invoices/203)

    try:
        r = requests.get(
            url="https://api.fortnox.se/3/invoices?customername="+str(custumer_name), 
            headers = headers,
        )

    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
    return r.content

def seekOrderByNumber(headers, number):
    # Invoices (GET https://api.fortnox.se/3/invoices/203)

    try:
        r = requests.get(
            url="https://api.fortnox.se/3/invoices/"+str(number)+"/", 
            headers = headers,
        )

    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
    return r.content


def seekOrderByOrderNumber(headers, order_number):
    url = "https://api.fortnox.se/3/invoices?yourreference="+str(order_number)

    try:
        r = requests.get(
            url=url, 
            headers = headers,
        )
    
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

    return r.content

def createOrder(headers, customer_order):
    try:
        r = requests.post(
            url="https://api.fortnox.se/3/invoices",
            headers = headers,
            data = customer_order,
        )

        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

# this is the order
def createNewOrder(headers, customer_new_order, order_number=''):

    try:
        r = requests.post(
            url="https://api.fortnox.se/3/orders",
            headers = headers,
            data = customer_new_order,
        )
        print r.content
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

# make invoice from order
def InvoicefromOrder(headers, order_number=''):
    try:
        r = requests.put(
            url="https://api.fortnox.se/3/orders/"+ str(order_number) +"/createinvoice",
            headers = headers,
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

def EmailOrder(headers, order_number=''):
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/orders/"+ str(order_number) +"/email",
            headers = headers,
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')    

# Get all articles
def get_articles(headers, page):
    # Articles (GET https://api.fortnox.se/3/articles)
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/articles/?page="+page,
            headers = headers
        )

    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

    return r.content
 

def get_article(headers, article_num):
    # Article (GET https://api.fortnox.se/3/articles/TR01)
    try:
        art_int = int(article_num)
    except: 
        pass

    art_int_str = str(article_num)

    try:
        r = requests.get(
            url="https://api.fortnox.se/3/articles/"+ str(art_int_str) ,
            headers = headers,
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')


def create_article(articleNumber, data, headers):
    # Articles (POST https://api.fortnox.se/3/articles)

    try:
        r = requests.post(
            url="https://api.fortnox.se/3/articles",
            headers = headers ,
            data = data
            )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')


def delete_article(headers, articleNumber):
    # Article (DELETE https://api.fortnox.se/3/articles/FRPPLUS)

    try:
        r = requests.delete(
            url="https://api.fortnox.se/3/articles/"+articleNumber,
            headers = headers ,
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

    
# Update article
def update_article(articleNumber, data, headers):
    # Article (PUT https://api.fortnox.se/3/articles/DE_782)
    
    try:
        r = requests.put(
            url="https://api.fortnox.se/3/articles/" + articleNumber,
            headers = headers ,
            data = data
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

# Request: Accounts (https://api.fortnox.se/3/accounts)
connection = httplib.HTTPSConnection('api.fortnox.se', 443, timeout = 30)

# Headers
# get accounts
def get_acconts():
	connection.request('GET', '/3/accounts', None, headers_)
	try:
		response = connection.getresponse()
		content = response.read()
		# Success
		print('Response status ' + str(response.status))
     	#print('Response status ' + str(content))
     
	except httplib.HTTPException, e:
		# Exception
		print('Exception during request')

def formatJson(the_json):
    try:
        the_json = the_json.replace('u\'', '"')
    except:
        pass
    try:
        the_json = the_json.replace('\'', '"')
    except:
        pass
    return the_json

def formatJson2(the_json):
    the_json = json.dumps(the_json)
    try:
        the_json = the_json.replace('u', '')
    except:
        pass
    try:
        the_json = the_json.replace('\'', '"')
    except:
        pass
    the_json = json.loads(the_json)
    return the_json

def article_for_csv(csv_path): 
    with open(csv_path) as f:
        reader = csv.reader(f)
    
        # loop all the articles
        headers = get_headers()
        process_json = []

        for article in reader:
            # crate a json article from csv row
            print article[1]

            articleNumber = article[0]
            data = json.dumps({
                "Article": {
                    "Description": article[1],
                    "ArticleNumber": article[0],
                    "Unit": 'st',
                    "QuantityInStock": article[2]
                }
            })
            #process_json.append({"art_json_fail": article[1]})
                
            # try to insert the article 
            # surrund this in a try except soon  
            returns = create_article(articleNumber, data, headers)
            r = json.loads(returns)

            if 'ErrorInformation' in r:  
                process_json.append({"insert_fail": article[0]})
                update = 1
            else: 
                process_json.append({"insert_success": article[0]}) 
                update = 0


            # if the article failed i can alreay be in fortnox, then try to update
            if (update == 1): 

                returns = update_article(articleNumber, data, headers) 
                r = json.loads(returns)

                if 'ErrorInformation' in r:  
                    process_json.append({"update_fail": article[0]})
                else: 
                    process_json.append({"update_success": article[0]}) 

            print process_json

# stock logic 
def stockvalue_down(article_num): 
    update = 1
    headers = get_headers()
    process_json = []
    retured_art = get_article(headers, article_num)

    art_json = json.loads(retured_art)
  
    if 'ErrorInformation' in art_json:  
        process_json.append({"insert_fail": article[0]})
        update = 0
    else: 
        amount = int(art_json['Article']['QuantityInStock'])
        amount = amount - 1  
        data = json.dumps({
                "Article": {
                    "ArticleNumber": article_num, 
                    "QuantityInStock": amount
                }
            })
        art_returns = update_article(article_num, data, headers)
    if update == 1: 
        return art_returns
    else:
        return "at this point something failed"    

def get_stockvalue(article_num):
    headers = get_headers()
    article = get_article(headers, article_num)
    json_article = json.loads(article)
    art_stock_int = json_article["Article"]["QuantityInStock"]
    return art_stock_int

# running som tests 

def articel_test(): 
    headers_ = get_headers()
    article_num_ = get_art_temp()
    article = get_article(headers_, article_num_)
    print "Printing Article: ---" 
    print article 
    print "EndArticle: ---"

def get_customer():
    temp_Customer = get_testCustomer() 
    print temp_Customer

def create_customer_test(): 
    print "Printing Test-Custumer ---  " 
    headers = get_headers()
    temp_Customer = get_testCustomer()
    response = CreateCostumer(headers, temp_Customer)
    print response
    print "EndTest-Customer --- "
 
def search_customer(): 
    print "Searching Customer ---  " 
    headers = get_headers()
    searchInfo_customer = searchCustomer(headers, "Palle Torsson", "palle.torsson@gmail.com")
    print searchInfo_customer 
    return searchInfo_customer
    print "EndSearch --- " 


def update_customer_test(): 
    headers = get_headers()
    customer = get_testCustomer()
    customer_url = "https://api.fortnox.se/3/customers/49"
    update_costumer = updateCostumer(headers, customer, customer_url)
    print update_costumer
    print "EndTest-Create or update --- " 


def update_or_create_customer_test(): 
    headers = get_headers()
    customer = get_testCustomer()
    create_costumer = customerExistOrCreate(headers, customer)
    print create_costumer
    print "EndTest-Create or update --- " 

def create_order_test(): 
    headers = get_headers()
    customer_order = json.dumps({
                "Invoice": { 
                    "InvoiceRows": [{
						"DeliveredQuantity": 1,
						"ArticleNumber": "9901",	
					},
					{
						"DeliveredQuantity": 1,
						"ArticleNumber": "2",	
					},
					],
                    "CustomerNumber": 24, 
                    "PriceList": "B",
					"Comments": "payexid 73847320",
                    "YourOrderNumber": 3875297,                   
                }
            })  
    order = createOrder(headers, customer_order)
    print order
  
#"Comments": payexid,
#"YourOrderNumber": orderid,

if local_tests == True: 
    print "Running Tests: "
    #create_customer_test()
    print "End Testing --- " 


