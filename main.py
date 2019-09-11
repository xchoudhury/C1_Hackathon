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

def create_savings_account():
    url = base_url + 'customers/{}/accounts'.format(customerId)
    payload = {
    "type": "Savings",
    "nickname": "test",
    "rewards": 10000,
    "balance": 10000,	
    }
    # Create a Savings Account
    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        params={'key': apiKey}
        )

    if response.status_code == 201:
        print('account created')
    else:
        print(response.text)

def main():
    lat = 38.89
    lng = -77.12
    rad = 2
    atms = get_atms(lat, lng, rad)
    print(atms)
        
if __name__ == "__main__":
    main()