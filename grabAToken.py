import json
import requests
import datetime
import tokenRefresh

def getToken():
    f = open('/home/magicmoney/ebay/usr.tok', 'r')
    tokens = json.load(f)
    f.close()

    if datetime.datetime.today() > datetime.datetime.strptime(tokens['expiry'], '%Y-%m-%d %H:%M:%S.%f'):
        tokenRefresh.refresh()
        f = open('usr.tok', 'r')
        tokens = json.load(f)
        f.close()

    return tokens['token']

if __name__ == '__main__':
    getToken()
