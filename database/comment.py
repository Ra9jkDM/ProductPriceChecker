from sqlalchemy.orm import Session
from models import ENGINE, Comment, User

def create_comment(product_id, user_id, comment, stars):
    id = -1
    with Session(autoflush=True, bind=ENGINE) as db:
        comment = Comment(product_id = product_id, user_id = user_id, comment = comment, stars = stars)
        db.add(comment)
        db.commit()

        id = comment.id

    return id

def delete_comment(id):
    with Session(autoflush=True, bind=ENGINE) as db:
        comment = db.query(Comment).filter_by(id=id).first()
        db.delete(comment)
        db.commit()

def get_user(id):
    user = User(id=-1)
    with Session(autoflush=True, bind=ENGINE) as db:
        user = db.query(Comment).filter_by(id=id).first().user
    
    return user