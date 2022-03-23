import requests
import json

def jprint(obj):
	text = json.dumps(obj, sort_keys = True, indent = 4)
	print(text)

api_url_local = "http://localhost:8000"
api_url_online = "https://fastapi-ej21.herokuapp.com"

response1 = requests.get(api_url_local)
dictionnaire1 = response1.json()
jprint(dictionnaire1)

to_push = {"email": "ndang@example.com", "password":"2001"}

response2 = requests.post(api_url_local+"/users", json=to_push)
dictionnaire2 = response2.json()
jprint(dictionnaire2)

#to_push = {"username": "ndang@example.com", "password":"2001"}
#response3 = requests.post(api_url_local+"/login", json=to_push)
#dictionnaire3 = response3.json()
#jprint(dictionnaire3)