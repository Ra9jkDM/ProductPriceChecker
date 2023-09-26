from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, select, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, mapped_column, Mapped, relationship

from typing import List
from datetime import datetime, date

engine = create_engine("sqlite:///test.db")#, echo=True)
conn = engine.connect() 

# Create DB

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String ,unique=True, nullable=False)
    description: Mapped[String] = mapped_column(String, nullable=True)
    image: Mapped[String] = mapped_column(String, nullable=True)

    urls: Mapped[List["Url"]] = relationship()
    comments: Mapped[List["Comment"]] = relationship()

class Shop(Base):
    __tablename__ = "shop"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[String] = mapped_column(String, unique=True, nullable=False)

    urls: Mapped[List["Url"]] = relationship()

class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"),primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"), primary_key=True)

    url: Mapped[String] = mapped_column(String, nullable=False)

    product: Mapped[List["Product"]] = relationship()
    shop: Mapped[List["Shop"]] = relationship()
    prices: Mapped[List["ProductPrice"]] = relationship()


class ProductPrice(Base):
    __tablename__ = "product_price"

    url_id: Mapped[int] = mapped_column(ForeignKey("url.id"), primary_key=True)
    date: Mapped[Date] = mapped_column(Date, primary_key=True)

    price:Mapped[int] = mapped_column(Integer)

    url: Mapped[List["Url"]] = relationship()


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String, nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship()

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[String] = mapped_column(String, nullable=False, unique=True)

    sault: Mapped[String] = mapped_column(String, nullable=False) # Соль
    password: Mapped[String] = mapped_column(String, nullable=False) # Хеш пароля

    # sault + password | use SHA1, SHA512

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)

    firstname: Mapped[String] = mapped_column(String, nullable=False)
    lastname: Mapped[String] = mapped_column(String, nullable=False)
    active: Mapped[Boolean] = mapped_column(Boolean, default=True)

    role: Mapped["Role"] = relationship()
    comments: Mapped[List["Comment"]] = relationship()
    
class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    comment: Mapped[String] = mapped_column(String, nullable=False)
    stars: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped["Product"] = relationship()
    user: Mapped["User"] = relationship()

# class Parent(Base):
#     __tablename__ = "parent_table"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[List["Child"]] = relationship()
#     name: Mapped[String] = mapped_column(String)


# class Child(Base):
#     __tablename__ = "child_table"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
#     price: Mapped[int] = mapped_column(Integer)



Base.metadata.create_all(bind=engine)



with Session(autoflush=True, bind=engine) as db:
    # p1 = Product(id=1, name='Hi tech')
    # p2 = Product(id=2, name='Hi Chech')

    # s1 = Shop(id=1, name='DNS')
    # s2 = Shop(id=2, name='Citilink')
    # s3 = Shop(id=3, name='Regard')

    # u1 = Url(id=1,product_id=p1.id, shop_id=s1.id, url='https://product1')
    # u2 = Url(id=2,product_id=p1.id, shop_id=s2.id, url='https://product1&shop=2')
    # u3 = Url(id=3,product_id=p1.id, shop_id=s3.id, url='https://product1&shop=3')

    # u4 = Url(id=4,product_id=p2.id, shop_id=s1.id, url='https://product1001')

    # pp1 = ProductPrice(url_id=u1.id, date=datetime.now(), price=100)
    # pp2 = ProductPrice(url_id=u2.id, date=datetime.now(), price=110)
    # pp3 = ProductPrice(url_id=u3.id, date=datetime.now(), price=200)

    # pp5 = ProductPrice(url_id=1, date=date(2022, 12, 1), price=80)
    # pp6 = ProductPrice(url_id=2, date=date(2022, 12, 1), price=40)
    # pp7 = ProductPrice(url_id=3, date=date(2022, 12, 1), price=65)

    # pp4 = ProductPrice(url_id=u4.id, date=datetime.now(), price=80)

    # db.add(p1)
    # db.add(p2)

    # db.add(s1)
    # db.add(s2)
    # db.add(s3)

    # db.add(u1)
    # db.add(u2)
    # db.add(u3)
    # db.add(u4)
 
    # db.add(pp1)
    # db.add(pp2)
    # db.add(pp3)
    # db.add(pp4)
    # db.add(pp5)
    # db.add(pp6)
    # db.add(pp7)

    # db.commit()


    # # urls = db.query(Url).all()

    # # for i in urls:
    # #     print(i.product.name, i.shop.name, i.url)
    # #     for j in i.price:
    # #         print(f"Price: {j.price}")


    # r1 = Role(id=1, name="Admin")
    # r2 = Role(id=2, name="User")

    # user_1 = User(email="reer@gmail.com", sault="yue", password="1230r002", role_id=1, firstname="Bob", lastname="Rore")
    # user_2 = User(email="mic@gmail.com", sault="ay3", password="admin123", role_id=2, firstname="BIB", lastname="Case")

    # db.add(r1)
    # db.add(r2)
    # db.add(user_1)
    # db.add(user_2)
    # db.commit()

    # user = db.query(User).first()
    # print(user.firstname, user.role.name, user.active)

    # # ToDo Test comments in rable 'Product'
    # c1 = Comment( product_id=1, user_id=1, comment="Good product", stars=5)
    # c2 = Comment(product_id=1, user_id=2, comment="do not shure it is good", stars=2)

    # db.add(c1)
    # db.add(c2)
    # db.commit()




    products = db.query(Product).all()

    for i in products:
        print(i.name)
        for j in i.urls:
            price = sorted(j.prices, key=lambda price: price.date, reverse=True)
            print(f'\t{j.shop.name} {j.url} {price[0].price}')
        
        print("Comments:")
        for j in i.comments:
            print(f"\t{j.user.firstname}: {j.comment}| {j.stars}")


    print('\n\n\nCheck')
    prices = db.query(ProductPrice).order_by(ProductPrice.date.desc())
    for i in prices:
        print(i.url.product.name, i.date, i.price)


    # for i in table_join:
    #     print(*i)

#     # parent_1 = Parent(id=44, name = 'Bob')
#     # parent_2 = Parent(id=43, name = 'Tom')

#     # # db.add(parent_1)
#     # # db.add(parent_2)

#     # child_1 = Child(parent_id=parent_1.id, price=2000)
#     # child_2 = Child(parent_id=parent_2.id, price=25)

    
    
#     # db.add(child_1)
#     # db.add(child_2)
  

#     # db.commit()


#     parent = db.query(Parent).filter(Parent.name == "Tom", Parent.id > 3).first()
#     print(parent.id)
#     for i in parent.children:
#         print(i.id, i.price)



   

