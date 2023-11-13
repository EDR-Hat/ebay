import requests
import base64
import json
from urllib.parse import unquote

endpoint = "https://auth.ebay.com/oauth2/authorize"

scope = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly"

creds = {}
print('enter the client_id')
creds['client_id'] = str(input())
print('enter the client_secret')
creds['client_secret'] = str(input())
print('enter the redirect_uri')
creds['redirect_uri'] = str(input())

print('navigate to the following url and grant our application access')
print(endpoint + '?client_id=' + creds['client_id'] + '&response_type=code&redirect_uri=' + creds['redirect_uri'] + '&scope=' + scope)

endpoint = 'https://api.ebay.com/identity/v1/oauth2/token'
headers = {}
identifier = 'Basic ' + base64.b64encode(bytes( creds['client_id'] + ':' + creds['client_secret'], 'utf-8')).decode('utf-8')

f = open('auth.cred', 'w')
f.write(identifier)
f.close()

headers["Content-Type"] = 'application/x-www-form-urlencoded'
headers['Authorization'] = identifier

payload = {}
payload['redirect_uri'] = creds['redirect_uri']
payload['grant_type'] = 'authorization_code'
print("paste the url within 2 minutes")
url = unquote(str(input()))
payload['code'] = url.split('&')[2].split('=')[1]
r = requests.post(endpoint, headers=headers, data=payload)

if r.status_code != 200:
    print(payload)
    print(r)
    print(r.status_code)
    print(r.json)
    print(r.text)
    print(r.headers)
    print('non okay response received')
    exit(1)

f = open('tokens', 'w')
tokens = r.json()
f.write(json.dumps(tokens))
f.close()
