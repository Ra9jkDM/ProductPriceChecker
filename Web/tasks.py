from threading import Thread
from time import sleep
from datetime import datetime

from .views.proxy import dollar, currencies, get_price
from .database import currency, url, product_price

def update_currency_thread():
    while True:
        update_currency()     
        sleep(12*60*60)

def update_product_price_thread():
    while True:
        update_prices()
        sleep(24*60*60)



def update_currency():
    print("Update currencies")
    items = currency.get_currencies()
    print(items)
    for i in items:
        result = currencies(None, i["code"])



def update_prices():
    print("Update price")
    urls = url.get_urls()

    i = 0
    while i < len(urls):
        tmp = urls[i:i+6]
        data = get_price(tmp)

        product_price.add_new_prices(data["shops"])
        i+=6


currency_thread = Thread(target = update_currency_thread)
price_thread = Thread(target = update_product_price_thread)



