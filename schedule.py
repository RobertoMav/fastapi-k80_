from functions import to_json
import requests

def post():
    data = to_json()
    request = requests.post("https://fastapi-production-549d.up.railway.app/data/", data=data)
    return request, request.json()

post()