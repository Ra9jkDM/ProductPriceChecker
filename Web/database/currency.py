from sqlalchemy.orm import Session
from Web.models import ENGINE, Currency, ExchangeRates

def _date_to_str(date):
    return date.strftime("%Y-%m-%d")

def get_price(date, currency_name="Доллар"):
    price = -1
    date = _date_to_str(date)

    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currency_id = db.query(Currency).filter(Currency.name == currency_name).first().id
            exchange_rate = db.query(ExchangeRates).filter(ExchangeRates.date == date, ExchangeRates.currency_id == currency_id).first()

            if not exchange_rate == None:
                price = exchange_rate.price
    except:
        pass

    return price

def save_price(date, price, currency_name="Доллар"):
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            currency_id = db.query(Currency).filter(Currency.name == currency_name).first().id
            
            db.add(ExchangeRates(date=date, currency_id=currency_id, price=price))
            db.commit()
    except:
        pass