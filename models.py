from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey, select, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, mapped_column, Mapped, relationship, backref

from flask_login import UserMixin

from typing import List
from datetime import datetime, date

from os import environ

import random


USERNAME = environ.get("database_username") 
PASSWORD = environ.get("database_password")

HOST = environ.get("database_host")
PORT = int(environ.get("database_port"))

DATABASE = environ.get("database_name")
DIALECT = environ.get("database_dialect")


ENGINE = create_engine(f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}") #, echo=True)


Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[String] = mapped_column(String(100) ,unique=True, nullable=False)
    description: Mapped[String] = mapped_column(String(2000), nullable=True)
    image: Mapped[String] = mapped_column(String(1000), nullable=True)

    urls: Mapped[List["Url"]] = relationship()
    comments: Mapped[List["Comment"]] = relationship()

class Shop(Base):
    __tablename__ = "shop"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name:Mapped[String] = mapped_column(String(100), unique=True, nullable=False)

    urls: Mapped[List["Url"]] = relationship()

class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id", ondelete="CASCADE"), primary_key=True)

    url: Mapped[String] = mapped_column(String(500), nullable=False)

    product: Mapped[List["Product"]] = relationship('Product', backref=backref('url', passive_deletes=True))
    shop: Mapped[List["Shop"]] = relationship('Shop', backref=backref('url', passive_deletes=True))
    prices: Mapped[List["ProductPrice"]] = relationship()


class ProductPrice(Base):
    __tablename__ = "product_price"

    url_id: Mapped[int] = mapped_column(ForeignKey("url.id", ondelete="CASCADE"), primary_key=True)
    date: Mapped[Date] = mapped_column(Date, primary_key=True)

    price:Mapped[int] = mapped_column(Integer)

    url: Mapped[List["Url"]] = relationship('Url', backref=backref('product_price', passive_deletes=True))


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[String] = mapped_column(String(100), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship()

class User(UserMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    email: Mapped[String] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[String] = mapped_column(String(500), nullable=False) # Хеш пароля

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)

    firstname: Mapped[String] = mapped_column(String(100), nullable=False)
    lastname: Mapped[String] = mapped_column(String(100), nullable=False)
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True)

    role: Mapped["Role"] = relationship()
    comments: Mapped[List["Comment"]] = relationship()
    
class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    comment: Mapped[String] = mapped_column(String(1500), nullable=False)
    stars: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped["Product"] = relationship('Product', backref=backref('comment', passive_deletes=True))
    user: Mapped["User"] = relationship('User', backref=backref('comment', passive_deletes=True))


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, unique=True)
    name: Mapped[String] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[String] = mapped_column(String(5), unique=True, nullable=False)

    exchange_rates: Mapped[List["ExchangeRates"]] = relationship()

class ExchangeRates(Base):
    __tablename__ = "exchange_rate"

    date: Mapped[Date] = mapped_column(Date, primary_key=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id", ondelete="CASCADE"), primary_key=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    currencies: Mapped["Currency"] = relationship('Currency', backref=backref('exchange_rate', passive_deletes=True))



# conn = ENGINE.connect() 


def add_test_data():
    products = ["Монитор Huawei MateView SE SSN-24 23.8", "Кофеварка KitFort КТ-715", 
                "Водоочиститель Аквафор Кристалл", "Кулер AEL LD-AEL-28c, напольный, электронный",
                 "Кондиционер Сплит-система CENTEK CT-65E12 настенная", "Швейная машина Janome Excellent Stitch 100",
                  "Сушилка для рук G-TEQ 8860 PS"]

    images = ["1.jpg", "2.jpg", "3.jpg", "4.jpg"]
    shops = ["Citilink", "Positronica", "Video-shoper", "Regard", "Y.market", "M.video"]

    roles = ["Admin", "User"]
    users = [["reer@gmail.com", 2, "Bob", "Rore"],
        ["lib@gmail.com", 2, "Tom", "Rom"],
        ["more@mail.ru", 2, "Lander", "Mos"], 
        ["qoe@gmail.com", 2, "Cress", "Zoop"],
        ["ads@yandex.ru", 1, "Adiv", "Urs"]]

    currencies = [{"name": "Доллар", "code": "USD"}, 
                {"name": "Евро", "code": "EUR"},
                {"name": "Казахстанских тенге", "code": "KZT"}]

    comments = ["The best product", "Not bad", "It's horrible", "Woow!", 'I can recommend this product']

    with Session(autoflush=True, bind=ENGINE) as db:
        
        for i, name in enumerate(roles, start=1):
            db.add(Role(name=name))

        for i, values in enumerate(users, start=1):
            db.add(User(email=values[0], password="test_pass", role_id=values[1], firstname=values[2], lastname=values[3]))


        for i, name in enumerate(products, start=1):
            db.add(Product(name=name, image=random.choice(images)))
            for j in range(random.randint(1, 8)):
                db.add(Comment(product_id=i, user_id=random.randint(1, len(users)), comment=random.choice(comments), stars=random.randint(0, 5)))
        
        for i, name in enumerate(shops, start=1):
            db.add(Shop(name=name))

        id = 1
        for i, value in enumerate(products, start=1):
            for j, name in enumerate(shops, start=1):
                db.add(Url(product_id=i, shop_id=j, url=f"https://{name}/{value}/"))
                for d in range(1, 11):
                    db.add(ProductPrice(url_id=id, date=date(2022, 12, 1+d), price=random.randint(2500, 55000)))

                id += 1

        

        for i, item in enumerate(currencies, start=1):
            db.add(Currency(name=item["name"], code=item["code"]))
            for j in range(1, 11):
                db.add(ExchangeRates(date=date(2022, 12, 1+j), currency_id=i, price=random.randint(2000, 20000)/100))
        

        db.commit()

def selection_of_db():
    with Session(autoflush=True, bind=ENGINE) as db:

        print('Товары:')
        products = db.query(Product).all()
        for i in products:
            print(i.name, i.image)
            for j in i.urls:
                price = sorted(j.prices, key=lambda price: price.date, reverse=True)
                print(f'\t{j.shop.name} {j.url}\t{price[0].price}')
            
            print("Comments:")
            for j in i.comments:
                print(f"\t{j.user.firstname}: {j.comment}| {j.stars}")

            print("\n\n")


        print("\nВалюты")
        u = db.query(Currency).all()
        for i in u:
            print(i.name)

            prices = sorted(i.exchange_rates, key=lambda x: x.date, reverse=True)

            for j in prices:
                print(f"\t{j.date} | {j.price}")

            print("\n\n")



if __name__ == "__main__":
    Base.metadata.create_all(bind=ENGINE)

    add_test_data()
    selection_of_db()

# python models.py