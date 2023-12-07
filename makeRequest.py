import json
import requests
import base64
import tokenRefresh
import grabAToken

def makeRequest(reqType, endpoint, headers, parameters=None, payload=None):
    match reqType.lower():
        case 'get':
            if parameters != None:
                r = requests.get(endpoint, headers, params=parameters)
            else:
                r = requests.get(endpoint, headers)
        case _:
            r = None
    return r
    

#need to write refresh token code, accidentally overwrote the refresh token and lost it!
auth = open('auth.cred', 'r').readline()
tok = grabAToken.getToken()
r = makeRequest('get', 'https://api.ebay.com/sell/negotiation/v1/find_eligible_items', {'Authorization': 'Bearer ' + tok, 'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'})
print(r.status_code)
print(r)
print(r.json)
print(r.text)
print(r.headers)
