import requests
import json
import requests
import httplib

# get your api setting
from local_fortnox import get_headers

# Request: Accounts (https://api.fortnox.se/3/accounts)
connection = httplib.HTTPSConnection('api.fortnox.se', 443, timeout = 30)

# Help functions
def get_stockquantity(product):
    # create the id for the request
    # the q: how are we goin to store the id 
    # say when a new rea object is created we store that in fortnox with an id based on artikelnumber_patter_color_quality_size_reaid
    stockquantity = fortnox_get_stockquantiy(id_)
    return stockquantity


# Create a json-object from givendata for update
def json_update(articleNumber, QuantityInStock): 
    data_ = json.dumps({
                "Article": {
                    "QuantityInStock": QuantityInStock,
                    "ArticleNumber": articleNumber,			
                }
            })
    return data_


# Interact with API
# Customers
# url such as : https://api.fortnox.se/3/customers?name=palle torsson
# Check if customer exit
def searchCustomer(headers, name, email): 
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/customers?name="+name+"&email="+email,
            headers = headers,
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')

# Create customer
def CreateCostumer(headers, customer): 
    try:
        r = requests.post(
        url="https://api.fortnox.se/3/customers",
            headers = headers,
            data = customer
        )
        return ('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')

# Update customer
def updateCostumer(headers, customer, customer_url):
    try:
        r = requests.put(
            url=customer_url,
            headers = headers,
            data = customer
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return('HTTP Request failed')

def createOrder(headers, customer_order):
    try:
        r = requests.post(
            url="https://api.fortnox.se/3/invoices",
            headers = headers,
            data = customer_order
        )

        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

# Articles logic
# Articles (GET https://api.fortnox.se/3/articles)
def get_articles(headers):
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
 
# Article (GET https://api.fortnox.se/3/articles/TR01)
def get_article(headers, article_num):
    article_num = get_art_temp()
    try:
        r = requests.get(
            url="https://api.fortnox.se/3/articles/"+ article_num ,
            headers = headers,
        )
        return r.content
    except requests.exceptions.RequestException as e:
        return ('HTTP Request failed')

# Articles (POST https://api.fortnox.se/3/articles)
def create_article(articleNumber, data, headers):
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

# Accounts logic
# get accounts
def get_acconts():
	connection.request('GET', '/3/accounts', None, headers_)
	try:
		response = connection.getresponse()
		content = response.read()
		# Success
		return context
	except httplib.HTTPException, e:
		# Exception
		return('Exception during request')


# If you want to run some requests from commandline set it to True
# $ python fortnox.py 
local_tests = True; 

# Force value of article for testing 
def get_art_temp(): 
    return "DE_782"

if local_tests == True: 
    # get headers
    headers_ = get_headers()
    # test article 
    article_num_ = get_art_temp()
    article = get_article(headers_, article_num_)
    print article 
    # test account 
    acconts = get_acconts()
    print accounts 

