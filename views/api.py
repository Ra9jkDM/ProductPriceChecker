from flask import Blueprint, request
from flask_login import login_required, current_user
import json

from .modules.decorators import is_admin

from database import product, comment, role

api = Blueprint("api", __name__)

@api.route("/products")
def get_products():
    return product.get_products()

@api.route("/product")
def get_product():
    id = request.args.get("id")
    result = product.get_product(id)
    return result

@api.route("/product", methods=["POST"])
@login_required
@is_admin
def add_product_post():
    json_data = _get_json_data(request.files["data"])
    json_data = json.loads(json_data)

    if request.files.get('image'):
        file = request.files['image']
    else:
        return {"status": "error"}

    result = product.save_product(json_data, file)
        
    return result

def _get_json_data(bytes_data):
    json_data = b''
    for i in bytes_data:
        json_data += i
    
    return json_data

@api.route("/add_comment", methods=["POST"])
@login_required
def add_comment():
    json_data = json.loads(request.data)
    id = comment.create_comment(json_data["product_id"], current_user.id, json_data["comment"], 3)
    return {"id": id, "name": current_user.firstname}

@api.route("/delete_comment", methods=["POST"])
@login_required
def delete_comment():
    json_data = json.loads(request.data)
    id = json_data["id"]
    user = comment.get_user(id)

    if role.is_admin(current_user) or current_user.id == user.id:
        comment.delete_comment(id)
        return {"status": "ok"}

    return {"status": "error"}

