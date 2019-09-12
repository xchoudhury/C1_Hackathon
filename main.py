import requests
import json

customerId = '5d72722a322fa016762f2f96'
apiKey = '3307ed298dcffa965a1c7fc50085ef47'
base_url = 'http://api.reimaginebanking.com'

def get_atms(lat=0, lng=0, rad=1):
    url = base_url + '/atms'
    params = {
        'key' : apiKey,
        'lat' : lat,
        'lng' : lng,
        'rad' : rad
    }
    resp = requests.get(
        url,
        headers={'content-type':'application/json'},
        params=params
    )

    data = resp.json()
    atms = []
    
    while data['data']:
        atms += data['data']
        
        url = base_url + data['paging']['next']
        resp = requests.get(
            url,
            headers={'content-type':'application/json'},
        )
        data = resp.json()

    return atms

def create_customer(payload):
    url = base_url + '/customers'

    params = {
        'key' : apiKey,
    }

    resp = requests.post(
        url,
        headers={'content-type':'application/json'},
        params=params,
        data=json.dumps(payload)
    )

    if not resp.ok:
        print(resp.reason)
        return resp.json()
    
    return resp.json()['objectCreated']

def create_credit_account(customerId):
    url = base_url + '/customers/{}/accounts'.format(customerId)
    payload = {
        "type": "Credit Card",
        "nickname": "Savor",
        "rewards": 500,
        "balance": 300,
    }
    # Create a Credit Card Account
    resp = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        params={'key': apiKey}
        )

    if not resp.ok:
        print(resp.reason)
        return resp.json()
    
    return resp.json()['objectCreated']

def create_bill(accountID):
    url = base_url + '/accounts/{}/bills'.format(accountID)
    payload = {
        'status' : 'pending',
        'payee' : 'Kaido Enterprise',
        'payment_amount' : 1738.42
    }

    # Create a bill
    resp = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        params={'key': apiKey}
        )

    if not resp.ok:
        print(resp.reason)
        return resp.json()
    
    return resp.json()['objectCreated']

def create_purchase(accountID):
    url = base_url + '/accounts/{}/purchases'.format(accountID)
    payload = {
        "merchant_id": "57cf75cea73e494d8675ec4b", # Apple Store
        "medium": "balance",
        "amount": 299.99,
        "status": "pending",
    }

    # Create a purchase
    resp = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        params={'key': apiKey}
        )

    if not resp.ok:
        print(resp.reason)
        return resp.json()
    
    return resp.json()['objectCreated']

def create_deposit(accountID):
    url = base_url + '/accounts/{}/deposits'.format(accountID)
    payload = {
        "medium": "balance",
        "amount": 100.00
    }

    # Create a deposit
    resp = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        params={'key': apiKey}
        )

    if not resp.ok:
        print(resp.reason)
        return resp.json()
    
    return resp.json()['objectCreated']

def main():
    # # Get all atms within a 2 mile radius of Mclean
    # # Long & Lat for Mclean
    # lat = 38.89
    # lng = -77.12
    # rad = 2
    # atms = get_atms(lat, lng, rad)
    # print(atms)

    # Create a Customer
    cust_info = {
        'first_name' : 'Luffy',
        'last_name' : 'Monkey',
        'address' : {
            'street_number' : '2222',
            'street_name': 'Ocean Lane',
            'city' : 'Water Seven',
            'state' : 'MI',
            'zip' : '48105'
        }
    }
    cust = create_customer(cust_info)
    print(cust)

    # Create a credit card for said customer
    credit_acc = create_credit_account(cust['_id'])
    print(credit_acc)

    # Create a bill for said credit card
    bill = create_bill(credit_acc['_id'])
    print(bill)

    # Create a purchase for said credit card
    purchase = create_purchase(credit_acc['_id'])
    print(purchase)

    # Create a deposit for said credit card
    deposit = create_deposit(credit_acc['_id'])
    print(deposit)

if __name__ == "__main__":
    main()