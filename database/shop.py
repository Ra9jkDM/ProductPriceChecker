from sqlalchemy.orm import Session
from models import ENGINE, Shop

def get_shops():
    shops = []
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            data = db.query(Shop).all()

            for i in data:
                shops.append({"id": i.id, "name": i.name})
    except:
        pass
    
    return shops