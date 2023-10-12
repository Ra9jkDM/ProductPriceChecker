from flask import Blueprint, render_template, make_response, request
from flask_login import login_required, current_user

from database import shop

from models import User

view = Blueprint("view", __name__)

@view.route("/")
def index():
    return render_template("index.html", name=_get_name())

@view.route("/about")
def about():
    return render_template("about.html", name=_get_name())

@view.route("/product")
def product():
    id = request.args.get("id")
    resp = make_response(render_template("product.html", name=_get_name(), id=id))
    resp.set_cookie('id', id, max_age=60)
    return resp

@view.route("/add_product")
@login_required
def add_product():
    data = shop.get_shops()
    return render_template("add_product.html", name=_get_name(), shops=data)

def _get_name():
    if isinstance(current_user, User):
        return current_user.firstname
    else:
        return None