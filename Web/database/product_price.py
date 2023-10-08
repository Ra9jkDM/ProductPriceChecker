from sqlalchemy.orm import Session
from Web.models import ENGINE, ProductPrice

from ..database.modules import date_controller

def add_new_prices(prices):
    try:
        now = date_controller.get_now()
        with Session(autoflush=True, bind=ENGINE) as db:
            for i in prices:
                db.add(ProductPrice(url_id=i["id"], date=now, price=i["price"]))
                db.commit()
    except:
        pass
