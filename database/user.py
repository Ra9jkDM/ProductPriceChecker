from sqlalchemy.orm import Session

from models import ENGINE, User

def get_user(email, password):
    with Session(autoflush=True, bind=ENGINE) as db:
        user = db.query(User).filter_by(email=email).first()
        return user