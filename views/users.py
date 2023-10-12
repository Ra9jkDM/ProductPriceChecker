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

    if not client:
        flash("Неверный логин или пароль.")
        return login()

    if not client.is_active:
        flash("Учетная запись отключена.")
        return login()

    login_user(client, remember=False)
    return redirect(url_for("view.index"))

@users.route("/registration")
@is_not_authenticated
def registration():
    return render_template("registration.html")

@users.route("/registration", methods=["POST"])
@is_not_authenticated
def registration_post():
    print("sun")
    form = request.form

    firstname = form.get("firstname")
    lastname = form.get("lastname")

    email = form.get("email")
    password = form.get("password")
    password_second = form.get("password_second")

    if not user.is_email_unique(email):
        flash("Аккаунт с таким адресом электронной почты существует.")
        return registration()
    
    if len(password) < 8:
        flash("Пароль должен содержать 8 символов")
        return registration()

    if password != password_second:
        flash("Пароли не совпадают")
        return registration()

    user.create_user(email, password, firstname, lastname)

    return login()


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("view.index"))



