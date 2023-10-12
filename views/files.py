from flask import Blueprint

from S3 import main as s3

file = Blueprint("files", __name__)

@file.route("/img/<name>")
def images(name):
    return _s3_get_files(f"img/{name}")

@file.route("/img/<path>/<name>")
def upload_images(path, name):
    return _s3_get_files(f"upload/{path}/{name}")

@file.route("/fonts/<name>")
def fonts(name):
    return _s3_get_files(f"fonts/{name}")


def _s3_get_files(path):
    try:
        file = s3.get_object(path)
        return file
    except:
        return "Error"