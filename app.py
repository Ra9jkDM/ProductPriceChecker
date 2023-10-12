from flask import Flask
from flask_login import LoginManager
from os import environ

from sqlalchemy.orm import Session

from models import ENGINE, User

from jinja_functions import register_jinja_functions

from tasks import update_currency_thread, update_product_price_thread

import urls
from threading import Thread

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

    register_login_manager(app)
    urls.register_blueprints(app)
    register_jinja_functions()

    # create_scheduled_tasks()

    return app

def register_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = "users.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        with Session(autoflush=True, bind=ENGINE) as db:
            return db.query(User).get(int(id))

def create_scheduled_tasks():
    currency_thread = Thread(target = update_currency_thread)
    price_thread = Thread(target = update_product_price_thread)

    currency_thread.start()
    price_thread.start()


def gen_secret_key():
    import secrets
    print(secrets.token_hex(20))

if __name__ == "__main__":
    # gen_secret_key()
    
    app = create_app()
    app.run(host="localhost", port=4500, debug=True)
