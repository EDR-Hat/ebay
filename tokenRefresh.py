import json
import requests

endpoint = 'https://api.ebay.com/identity/v1/oauth2/token'

headers = {}
headers['Content-Type'] = 'application/x-www-form-urlencoded'
f = open('auth.cred', 'r')
headers['Authorization'] = f.readlines()[0]
f.close()

f = open('tokens', 'r')
tokens = json.loads(f.readlines()[0])
f.close()
payload = {}
payload['refresh_token'] = tokens['refresh_token']
payload['grant_type'] = 'refresh_token'
payload['scope'] = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly"

r = requests.post(endpoint, headers=headers, data=payload)

if r.status_code != 200:
    print(payload)
    print(r)
    print(r.status_code)
    print(r.json)
    print(r.text)
    print(r.headers)
    print('response not a 200')
    exit(1)

f = open('tokens', 'w')
tokens = r.json()
f.write(json.dumps(tokens))
f.close()
