import jinja2

from database import role

def register_jinja_functions():
    jinja2.filters.FILTERS["is_admin"] = role.is_admin