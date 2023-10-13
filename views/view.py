from flask import Blueprint, render_template, make_response, request
from flask_login import login_required, current_user

from .modules.decorators import is_admin
from .modules import current_user_fields as user

from database import shop

from models import User

view = Blueprint("view", __name__)

@view.route("/")
def index():
    return render_template("index.html", name=user.get_name())

@view.route("/about")
def about():
    return render_template("about.html", name=user.get_name())

@view.route("/product")
def product():
    id = request.args.get("id")
    resp = make_response(render_template("product.html", name=user.get_name(), id=id, user_id = user.get_id()))
    return resp

@view.route("/add_product")
@login_required
@is_admin
def add_product():
    data = shop.get_shops()
    return render_template("add_product.html", name=user.get_name(), shops=data, id=-1)

@view.route("/edit_product")
@login_required
@is_admin
def edit_product():
    id = request.args.get("id")
    data = shop.get_shops()
    return render_template("add_product.html", name=user.get_name(), shops=data, id=id)