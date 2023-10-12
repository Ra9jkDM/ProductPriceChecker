from sqlalchemy.orm import Session
from enum import Enum

from models import ENGINE, Role

class Roles(Enum):
    admin = "Admin"
    user = "User"


def get_role(role):
    with Session(autoflush=True, bind=ENGINE) as db:
        return db.query(Role).filter_by(name=role.value).first()

def is_admin(user):
    if user.role_id == get_role(Roles.admin).id:
        return True
    return False
