from sqlalchemy.orm import Session
from Web.models import ENGINE, Currency, Product

def _get_price(urls):
    prices = []
    for i in urls:
        price = sorted(i.prices, key=lambda price: price.date, reverse=True)
        prices.append({"name": i.shop.name, "price": price[0].price})
    
    return prices

def _get_currency(currencies):
    result = []
    
    for i in currencies:
        prices = sorted(i.exchange_rates, key=lambda x: x.date, reverse=True)
        result.append({"name": i.name, "price": prices[0].price})

    return result

def get_products():
    result = []
    currencies = []
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            products = db.query(Product).all()
            currencies = _get_currency(db.query(Currency).all())

            for i in products:
                prices = _get_price(i.urls)
                p = {
                    "product_id" : i.id,
                    "image": f"img/products/{i.image}",
                    "name": i.name,
                    "prices": prices,
                }

                result.append(p)
    except:
        pass

    return {"products": result, "currencies":currencies}
