import requests
import json
URL = "http://127.0.0.1:5000/mail/"

headers = {'content-type': 'application/json','Authorization': u'Bearer fake_token_123'}
def post_data():
    data = '{"id":"testemail","password":"password"}'
    # json_data = json.dumps(data)
    # print(json_data)
    r = requests.post(url=URL,data=data,headers=headers)
    data = r.json()
    print(data)
post_data()