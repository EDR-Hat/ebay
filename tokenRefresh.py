import json
import requests
import datetime

def refresh():
    endpoint = 'https://api.ebay.com/identity/v1/oauth2/token'

    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    f = open('auth.cred', 'r')
    headers['Authorization'] = f.readline()
    f.close()

    f = open('ref.tok', 'r')
    tokens = json.load(f)
    f.close()
    payload = {}
    payload['refresh_token'] = tokens['token']
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

    tokens = r.json()
    usr = {}
    usr['token'] = tokens['access_token']
    usr['expiry'] = str(datetime.datetime.today() + datetime.timedelta(seconds=int(tokens['expires_in'])) )
    f = open('usr.tok', 'w')
    json.dump(usr, f)
    f.close()

if __name__ == '__main__':
    refresh()
