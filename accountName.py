import makeRequest

endpoint = 'https://apiz.ebay.com/commerce/identity/v1/user/'
r = makeRequest.makeRequest('get', endpoint, {})

match r.status_code:
    case 200:
        name = r.json()['username']
    case _:
        print("error status code was: " + str(r.status_code))
        exit(1)


