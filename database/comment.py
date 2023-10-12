from sqlalchemy.orm import Session
from models import ENGINE, Comment

def create_comment(product_id, user_id, comment, stars):
    with Session(autoflush=True, bind=ENGINE) as db:
        db.add(Comment(product_id = product_id, user_id = user_id, comment = comment, stars = stars))
        db.commit()