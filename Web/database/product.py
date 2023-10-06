from sqlalchemy.orm import Session
from Web.models import ENGINE, Currency, ExchangeRates, Product, ProductPrice, Shop, Url

from ..database.modules import date_controller

from ..S3 import main as s3

IMAGE_PATH = "Web/upload"
CURRENT_PATH = "products"

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




def _fill_urls_prices_labels(product):
    urls = []

    isFilled = False
    labels = []

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
    
    return urls, labels, datasets

def _fill_dollar_price(db, start_day, currency_name):
    dollar = []

    first_date = date_controller.get_yesterday(start_day)
    currency_id = db.query(Currency).filter(Currency.name == currency_name).first().id
    currency_price = db.query(ExchangeRates).filter(ExchangeRates.currency_id == currency_id,
                                    ExchangeRates.date >= first_date).order_by(ExchangeRates.date.asc()).all()

    for i in currency_price:
        dollar.append(i.price)

    return dollar

def _fill_comments(product):
    comments = []
    for i in product.comments:
        comments.append({"name": i.user.firstname, "lastname": i.user.lastname, "description": i.comment})
    
    return comments



def get_product(id, currency_name = "Доллар"):
    result = {}

    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            product = db.query(Product).filter(Product.id == id).first()


            urls, labels, datasets = _fill_urls_prices_labels(product)
            dollar = _fill_dollar_price(db, labels[0], currency_name)
            comments = _fill_comments(product)

            

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
    except:
        pass
    
    return result


def _get_extension(file):
    return str(file).split(".")[-1]

def _save_image(file, name):
    ext = _get_extension(file)
    filename = f"{name}.{ext}"
    s3.upload_object(CURRENT_PATH, filename, file)
    
    return f"{name}.{ext}"

def save_product(data, file):
    result = {"status": "ok"}
    try:
        if data["name"]=="":
            raise Exception("Empty name")
        with Session(autoflush=True, bind=ENGINE) as db:
            product = Product( name=data["name"], description = data["description"])
            db.add(product)
            db.commit()
            print(product.id)

            # Save image
            image_name = _save_image(file, product.id)
            product.image = image_name
            db.commit()

            # Save url
            for i in data["urls"]:
                shop_id = db.query(Shop).filter(Shop.name == i["name"]).first().id
                url = Url(product_id=product.id, shop_id=shop_id, url=i["url"])
                db.add(url)
                db.commit()

                now = date_controller.get_now()
                db.add(ProductPrice(url_id=url.id, date=now, price=i["price"]))

            db.commit()
    except:
        result["status"]="error"
    
    return result
        
        
       
