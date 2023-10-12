from sqlalchemy.orm import Session
from models import ENGINE, Currency, ExchangeRates

from database.modules import date_controller



def get_currencies():
    result = []
    with Session(autoflush=True, bind=ENGINE) as db:
        currensies = db.query(Currency).all()

        for i in currensies:
            result.append({"id": i.id,"name": i.name, "code": i.code})

    return result

def get_price(date, currency_code="USD"):
    price = -1
    date = date_controller.date_to_str(date)

    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currency_id = db.query(Currency).filter(Currency.code == currency_code).first().id
            exchange_rate = db.query(ExchangeRates).filter(ExchangeRates.date == date, ExchangeRates.currency_id == currency_id).first()

            if isinstance(exchange_rate, ExchangeRates):
                price = exchange_rate.price
    except:
        pass

    return price

def save_price(date, price, currency_code="USD"):
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currency_id = db.query(Currency).filter(Currency.code == currency_code).first().id
            db.add(ExchangeRates(date=date, currency_id=currency_id, price=price))
            db.commit()
    except:
        pass