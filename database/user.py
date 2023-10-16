from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from models import ENGINE, User, Role

from .role import get_role, Roles

def create_user(email, password, firstname, lastname):
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            role_id = get_role(Roles.user).id

            db.add(User(email=email, password=generate_password_hash(password, method="scrypt", salt_length=20), role_id=role_id, 
                        firstname=firstname, lastname=lastname,
                        is_active=True))
            db.commit()
    except:
        pass

def get_user(email, password):
    user = None
    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            user = db.query(User).filter_by(email=email).first()

        if isinstance(user, User) and check_password_hash(user.password, password):
            return user
    except:
        pass
    return None
    
def is_email_unique(email):
    user = None

    try:
        with Session(autoflush=True, bind=ENGINE) as db:
            user = db.query(User).filter_by(email=email).first()

        if isinstance(user, User):
            return False
    except:
        pass
    return True

    
