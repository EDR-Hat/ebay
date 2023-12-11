#import psycopg2 as psy
import pandas as pd
#import os
import math
import time
import datetime
import json
from makeRequest import makeRequest
import dateutil.parser

s = time.time()
#first draft won't use the database
#with open('db.cred', 'r') as f:
#    cred = json.load(f)
#f.close()

#conn = psy.connect(
#        host='localhost',
#        database="postgres",
#        user="postgres",
#        password=cred['secret']
#        )

#cur = conn.cursor()

offerController = pd.read_csv('directives/offers.csv')
endpoint = 'https://api.ebay.com/sell/negotiation/v1/find_eligible_items'
r = makeRequest('get', endpoint, {  'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'}, parameters={'limit': 200})
if r.status_code != 200:
    print(r.header)
    print(r.json())
    exit(1)

resp = r.json()
itms = [x['listingId'] for x in resp['eligibleItems']]

for itm in itms:
    endpoint = 'https://api.ebay.com/buy/browse/v1/item/'
    r = makeRequest('get', endpoint + '/v1|' + itm + '|0', {}, parameters={'fieldgroups': 'COMPACT'})
    if r.status_code != 200:
        continue
    resp = r.json()

    startTime = dateutil.parser.isoparse(resp['itemCreationDate'])
    price = float(resp['price']['value'])
    shipping = float(resp['shippingOptions'][0]['shippingCost']['value'])

    if shipping == 0:
        price = price - 5
    if price < 0:
        continue

    default = offerController[offerController['category'] == 'default'].loc[0]
    delay = (datetime.datetime.now(datetime.timezone.utc) - startTime).days
    aggPercent = default['dropPercentage'] * math.floor((delay - default['delay'])/ default['timeInterval'])
    if aggPercent < 0:
        aggPercent = 0
    offer1 = default['initial'] + aggPercent
    if offer1 > 1.0:
        offer1 = 0.5
    
    offer1 = price * offer1
    offer2 = price * default['maxOfferPercentage']
    finalOffer = max(offer1, offer2)

    load = {}
    #load['message'] = 'ebay suggests giving a customized message to each offer, apparrently it increases conversion. this might be worth doing some sort of formulaic one that is different than the ebay default'
    load['offeredItems'] = [ {'listingId': itm, 'price': { 'currency': 'USD', 'value': str(finalOffer)}, 'quantity': 1} ]
    load = json.dumps(load)

    endpoint = 'https://api.ebay.com/sell/negotiation/v1/send_offer_to_interested_buyers'
    r = makeRequest('post', endpoint, {'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US', 'Content-Type': 'application/json'}, payload=load)
    if r.status_code != 200:
        print(price)
        print(offer1)
        print(offer2)
        print(finalOffer)
        print(r.json())
        continue



e = time.time()
print(e - s)
    







#future idea is to simply grab data about the item from the database
#for now it uses data that's retrived from the api
#for each item id, follow the offer directive based on its settings
# -this might mean grabbing the price and time data for that item in the local database
# -basic directive should take into account time first listed, current price and initial price
