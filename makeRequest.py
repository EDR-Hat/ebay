import json
import requests
import base64
import grabAToken
from urllib.parse import unquote
from urllib.parse import quote

def makeRequest(reqType, endpoint, headers, parameters=None, payload=None):
    tok = grabAToken.getToken()
    headers['Authorization'] = 'Bearer ' + tok
    match reqType.lower():
        case 'get':
            if parameters != None:
                r = requests.get(endpoint, headers=headers, params=parameters)
            else:
                r = requests.get(endpoint, headers=headers)
        case 'post':
            if payload == None:
                print('tried to post without payload!')
                r = None
            elif parameters != None:
                r = requests.post(endpoint, headers=headers, params=parameters, data=payload)
            else:
                r = requests.post(endpoint, headers=headers, data=payload)
        case _:
            r = None
    return r
