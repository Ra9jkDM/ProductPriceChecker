from flask import Blueprint, request
from flask_login import login_required

import requests
from os import environ
import json
from datetime import datetime

from database import product, currency

API_URL = environ.get("api_url")
proxy = Blueprint("proxy", __name__)

@proxy.route("/shops", methods=["POST"])
@login_required
def shops():
    req = json.loads(request.data.decode("utf-8"))
    resp = requests.post(f"{API_URL}/shops/get", json={"shops": req['urls']})
    json_response = json.loads(resp.text)
    
    return json_response

@proxy.route("/currencies")
# @login_required
def get_currency():
    code = request.args.get("code")
    return currencies(code)

def currencies(code):
    now = datetime.now()
    item = currency.get(now, code)

    if item["price"] == -1:
        req = requests.get(f"{API_URL}/currency?codes={code}")
        item = json.loads(req.text)[0]
      
        currency.save_price(now, item["price"], item["code"])

    return item


def get_price(urls):
    resp = requests.post(API_URL+"/shops/get", json={"shops": urls})
    json_response = json.loads(resp.text)
    return json_response