import requests

url = 'http://localhost:5000/'
raw_data = {
    'alice_string':'100100001',
    'bob_string':'100000001',
}

x = requests.post(url, data = raw_data)

print(x.text)