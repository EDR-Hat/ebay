import math
import time
import datetime
import json
from makeRequest import makeRequest
import dateutil.parser

s = time.time()

def truncate(x):
    return x - x % 0.01

endpoint = 'https://api.ebay.com/sell/negotiation/v1/find_eligible_items'
r = makeRequest('get', endpoint, {  'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'}, parameters={'limit': 200})

match r.status_code:
    case 204:
        print('status code 204, no eleigible listings to send offers out')
        exit(0)
    case 200:
        pass
    case _:
        print(r.header)
        print(r.json())
        exit(1)

resp = r.json()
itms = [x['listingId'] for x in resp['eligibleItems']]

for itm in itms:
    endpoint = 'https://api.ebay.com/buy/browse/v1/item/'
    r = makeRequest('get', endpoint + '/v1|' + itm + '|0', {}, parameters={'fieldgroups': 'COMPACT'})
    if r.status_code != 200:
        print(r.status_code, itm)
        print("item search gave error code")
        continue
    resp = r.json()

    startTime = dateutil.parser.isoparse(resp['itemCreationDate'])
    price = float(resp['price']['value'])
    shipping = float(resp['shippingOptions'][0]['shippingCost']['value'])
    oldPrice = price

    if shipping == 0:
        price = price - 5
    if price < 1.04:
        print("price too low for an offer")
        continue

    load = {}
    #load['message'] = 'ebay suggests giving a customized message to each offer, apparrently it increases conversion. this might be worth doing some sort of formulaic one that is different than the ebay default'
    load['offeredItems'] = [ {'listingId': itm, 'discountPercentage': "5", 'quantity': 1} ]
    load = json.dumps(load)

    endpoint = 'https://api.ebay.com/sell/negotiation/v1/send_offer_to_interested_buyers'
    r = makeRequest('post', endpoint, {'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US', 'Content-Type': 'application/json'}, payload=load)
    if r.status_code != 200:
        print(itm)
        print(price)
        print(offer1)
        print(offer2)
        print(finalOffer)
        try:
            print(r.json())
        except:
            print('json not printable')
        continue



e = time.time()
print(e - s)
