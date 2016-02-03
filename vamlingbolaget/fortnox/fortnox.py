import requests
import json
import requests
import httplib
from local_fortnox import get_headers
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
    try: 
        order_json = json.dumps(order_json)
    except: 
        pass 

    order_json = formatJson(order_json)
    
    order_json = json.loads(order_json)

    invoicerows = []

    for item in order_json:
        try: 
           qu = str(order_json[item]['quantity'])
           ok = 1
        except:
           ok = 0 
           
        try: 
           art = str(order_json[item]['article'])
           ok = 1
        except:
           ok = 0
           

        if (ok == 1):
            invoicerows.append({
		        "DeliveredQuantity": qu,
		        "ArticleNumber": art, 
		      })

    # this is postal fee 
    invoicerows.append({
		        "DeliveredQuantity": 1,
		        "ArticleNumber": 2, 
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
        if local_tests == True:  
            print "Search responce "
            print r.content            
            print "Customer url: "
            try:
                print response_exist_json['Customers'][0]['@url']
            except: 
                print "no url"
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
    if local_tests == True:   
        print "customer json" 
        print customer 

    customer = formatJson(customer) 

    try:
        r = requests.post(
        url="https://api.fortnox.se/3/customers",
            headers = headers,
            data = customer
        )
        if local_tests == True: 
            print "Customer Created: "
            print r.content
            print customer

        customer = json.loads(r.content)

        if local_tests == True: 
            print "The custumer number"
            print customer['Customer']["CustomerNumber"]

        return customer['Customer']["CustomerNumber"]
    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')
 
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
        if local_tests == True:  
            print "customer is a dict" 
            print customer['Customer']  
    else:      
       customer = formatJson(customer)
     
    try:
        r = requests.put(
            url=customer_url,
            headers = headers,
            data = customer
        )

        if local_tests == True:  
            print "Printing the result for update Customer: "
            print r.content

        result = json.loads(r.content)

        if local_tests == True: 
            print "Update customer"
            print result['Customer']["CustomerNumber"]
        
        return result['Customer']["CustomerNumber"]

    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')

# Create or update customer
def customerExistOrCreate(headers, customer):
    customer_dict = json.loads(customer)
    # see if custumer exist, 
    customer_exist = searchCustomer(headers, customer_dict['Customer']['Name'], customer_dict['Customer']['Email']) 
    if local_tests == True:    
        print "does customer exist?:"
        print customer_exist 
        print customer 
        print customer_dict  

    if(customer_exist == False):
        try: 
            customer_response_id = CreateCostumer(headers, customer)
            if local_tests == True: 
                print "id, is none " 
                print customer_response_id
            return customer_response_id
        except: 
            customer_response = "Create error: " + str(customer_response)
       
    if(customer_exist != False):
        try:
            url = customer_exist
            #the returning result is customer id  
            customer_response_id = updateCostumer(headers, customer, url) 
            if local_tests == True: 
                print "id: " 
                print customer_response_id
            return customer_response_id
        except: 
            customer_response = "Update error: " + str(customer_response)

    return customer_response

def createOrder(headers, customer_order):
    try:
        r = requests.post(
            url="https://api.fortnox.se/3/invoices",
            headers = headers,
            data = customer_order,
        )
        if local_tests == True: 
            print r.content
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

# Get all articles
def get_articles(headers):
    # Articles (GET https://api.fortnox.se/3/articles)
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/articles",
            headers = headers ,
        )

        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

    response_data = json.dumps({ 
		"response": {
			"status_code" : r.status_code,
	        "content" : r.content 
		}
	})
    return response_data
 

def get_article(headers, article_num):
    # Article (GET https://api.fortnox.se/3/articles/TR01)
    article_num = get_art_temp()
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/articles/"+ article_num ,
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


