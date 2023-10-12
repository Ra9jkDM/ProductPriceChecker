from sqlalchemy.orm import Session
from models import ENGINE, Url

from database.modules import date_controller

def get_urls():
    result = []
    with Session(autoflush=True, bind=ENGINE) as db:
        data = db.query(Url).all()

        for i in data:
            result.append({"id": i.id, "name": i.shop.name, "url": i.url})

    return result