from sqlalchemy.orm import Session
from models import ENGINE, Currency, ExchangeRates

from database.modules import date_controller



def get_currencies():
    result = []
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currensies = db.query(Currency).all()

            for i in currensies:
                result.append({"id": i.id,"name": i.name, "code": i.code})
    except:
        pass
    return result

def get(date, currency_code="USD"):
    result = {"code": currency_code, "name": None, "price": -1}
    date = date_controller.date_to_str(date)

    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currency = db.query(Currency).filter(Currency.code == currency_code).first()
            exchange_rate = db.query(ExchangeRates).filter(ExchangeRates.date == date, ExchangeRates.currency_id == currency.id).first()

            if isinstance(exchange_rate, ExchangeRates):
                result["price"] = exchange_rate.price
                result["name"] = currency.name
    except:
        pass

    return result

def save_price(date, price, currency_code="USD"):
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currency_id = db.query(Currency).filter(Currency.code == currency_code).first().id
            db.add(ExchangeRates(date=date, currency_id=currency_id, price=price))
            db.commit()
    except:
        pass