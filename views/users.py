from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user, login_user, login_required, logout_user
from views.modules.decorators import is_not_authenticated

from database import user

users = Blueprint("users", __name__)


@users.route("/login")
@is_not_authenticated
def login():
    return render_template("login.html")

@users.route("/login", methods=["POST"])
@is_not_authenticated
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    client = user.get_user(email, password)

    if not client: # ToDo check pass
        flash("Неверный логин или пароль.")
        return redirect(url_for("users.login"))

    login_user(client, remember=False)
    return redirect(url_for("view.index"))

@users.route("/registration")
@is_not_authenticated
def registration():
    return render_template("registration.html")

@users.route("/registration")
@is_not_authenticated
def registration_post():
    pass # ToDo

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("view.index"))



