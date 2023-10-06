from django.urls import path
from django.http import JsonResponse, HttpResponse

import requests
import json
from datetime import datetime
from os import environ

from ..database import product, currency

API_URL = environ.get("API_URL")

def shops(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        resp = requests.post(API_URL+"/shops/get", json={"shops":req['urls']})
        json_response = json.loads(resp.text)
        return JsonResponse(json_response)
    return HttpResponseNotFound()



def currencies(request, code):
    now = datetime.now()
    item = {"price": currency.get_price(now, code)}

    if item["price"] == -1:
        req = requests.get(f"{API_URL}/currency?codes={code}")
        item = json.loads(req.text)[0]
      
        currency.save_price(now, item["price"], item["code"])

    return JsonResponse(item)


def dollar(request):
    return currencies(None, "USD")


proxy = [
    path("shops", shops),
    path("dollar", dollar),
]