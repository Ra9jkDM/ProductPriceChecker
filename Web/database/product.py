from sqlalchemy.orm import Session
from Web.models import ENGINE, Currency, ExchangeRates, Product

from datetime import datetime, date, timedelta

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

def _get_img_path(img):
    return f"/img/products/{img}"

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
                    "image": _get_img_path(i.image),
                    "name": i.name,
                    "prices": prices,
                }

                result.append(p)
    except:
        pass

    return {"products": result, "currencies":currencies}

def get_product(id, currency_name = "Доллар"):
    result = {}

    with Session(autoflush=True, bind=ENGINE) as db:
        product = db.query(Product).filter(Product.id == id).first()

        urls = []

        isFilled = False
        labels = []

        dollar = []
        datasets = []

        for i in product.urls:
            urls.append({"name": i.shop.name, "url": i.url, "price": i.prices[-1].price})

            price = []
            for j in i.prices:
                price.append(j.price)

                if not isFilled:
                    labels.append(str(j.date))

            isFilled = True

            datasets.append({"label": i.shop.name, "data":price, "borderWidth": 1})

        first_date = datetime.strptime(labels[0], "%Y-%m-%d") - timedelta(1)
        currency_id = db.query(Currency).filter(Currency.name == currency_name).first().id
        currency_price = db.query(ExchangeRates).filter(ExchangeRates.currency_id == currency_id,
                                    ExchangeRates.date >= first_date).order_by(ExchangeRates.date.asc()).all()
        # print(datetime.strptime(labels[0], "%Y-%m-%d"))

        for i in currency_price:
            dollar.append(i.price)

        comments = []
        for i in product.comments:
            comments.append({"name": i.user.firstname, "lastname": i.user.lastname, "description": i.comment})

        result = {
            "name": product.name,
            "description": product.description,
            "image": _get_img_path(product.image),
            "labels": labels,
            "urls": urls,
            "dollar": dollar,
            "datasets": datasets,
            "reviews": comments
        }

    return result