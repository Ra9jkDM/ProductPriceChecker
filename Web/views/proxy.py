from django.urls import path
from django.http import JsonResponse, HttpResponse

import requests
import json
from datetime import datetime

from ..database import product, currency

API_URL = "http://127.0.0.1:3000"

def shops(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        resp = requests.post(API_URL+"/shops/get", json={"shops":req['urls']})
        json_response = json.loads(resp.text)
        return JsonResponse(json_response)
    return HttpResponseNotFound()

def dollar(request):
    now = datetime.now()
    price = currency.get_price(now)

    if price == -1:
        req = requests.get(API_URL+"/currency/dollar")
        price = req.text

        currency.save_price(now, price)

    return HttpResponse(price)


proxy = [
    path("shops", shops),
    path("dollar", dollar),
]