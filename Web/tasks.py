from threading import Thread
from time import sleep
from datetime import datetime

from .views.proxy import dollar, currencies
from .database import currency, product

def threaded_function():
    while True:
        update_currency()     
        sleep(12*60*60)



def update_currency():
    print("Update currencies")
    items = currency.get_currencies()
    print(items)
    for i in items:
        result = currencies(None, i["code"])



def update_prices_task():
    print("Update price")
    # product.update_prices() # ToDo
    # tables: url, product_prices


thread = Thread(target = threaded_function)




