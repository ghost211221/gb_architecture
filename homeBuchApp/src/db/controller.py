from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, Float, String, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime 

from meta.singleton import Singleton

Base = declarative_base()

class ProductCategories(Base):
    __tablename__ = 'productcategories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    comment = Column(String)

    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return f'<ProductCategory({self.name}, {self.comment})>'

class ProductSubCategories(Base):
    __tablename__ = 'productsubcategories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(Integer, ForeignKey('productcategories.id'))
    comment = Column(String)

    productcategories = relationship('ProductCategories', uselist=True,
                                   cascade='delete,all')

    def __init__(self, name, category, comment=None):
        self.name = name
        self.category = category
        self.comment = comment

    def __repr__(self):
        return f'<ProductSubCategory({self.category}, {self.name}, {self.comment})>'

class Shops(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    inn = Column(String)
    address = Column(String)
    comment = Column(String)

    def __init__(self, name, inn, address, comment=None):
        self.name = name
        self.inn = inn
        self.address = address
        self.comment = comment

    def __repr__(self):
        return f'<Shop({self.name}, {self.inn}, {self.address}, {self.comment})>'

class Bills(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)
    fiscalNum = Column(String)
    dateTime = Column(DateTime)
    shop = Column(Integer, ForeignKey('shops.id'))
    total = Column(Float)
    comment = Column(String)

    shops = relationship('Shops', uselist=True, cascade='delete,all')

    def __init__(self, fiscalNum, dateTime, shop, total, comment=None):
        self.fiscalNum = fiscalNum
        self.dateTime = dateTime
        self.shop = shop
        self.total = total
        self.comment = comment

    def __repr__(self):
        return f'<Bill({self.fiscalNum}, {self.dateTime}, {self.shop}, {self.total}, {self.comment})>'

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(Integer, ForeignKey('productcategories.id'))
    subcategory = Column(Integer, ForeignKey('productsubcategories.id'))
    comment = Column(String)
    shop = Column(Integer, ForeignKey('shops.id'))
    price = Column(Float)
    date = Column(Date)

    productcategories = relationship('ProductCategories', uselist=True, cascade='delete,all')
    productsubcategories = relationship('ProductSubCategories', uselist=True, cascade='delete,all')
    shops = relationship('Shops', uselist=True, cascade='delete,all')

    def __init__(self, name, category, subcategory, shop, price, date, comment=None):
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.shop = shop
        self.price = price
        self.date = date
        self.comment = comment

    def __repr__(self):
        return f'<Product({self.name}, {self.category}, {self.subcategory}, {self.shop}, \
                          {self.price}, {self.date}, {self.comment})>'


class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    product = Column(Integer, ForeignKey('products.id'))
    bill = Column(Integer, ForeignKey('bills.id'))
    comment = Column(String)
    quantity = Column(Float)
    total = Column(Float)

    products = relationship('Products', uselist=True, cascade='delete,all')
    bills = relationship('Bills', uselist=True, cascade='delete,all')

    def __init__(self, product, bill, quantity, total, comment=None):
        self.product = product
        self.bill = bill
        self.quantity = quantity
        self.total = total
        self.comment = comment

    def __repr__(self):
        return f'<Purcahe({self.product}, {self.bill}, {self.quantity}, {self.comment})>'

class Controller():
    __metaclass__ = Singleton

    def __init__(self, db_engine):
        self.db_engine = db_engine
        Base.metadata.create_all(self.db_engine)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

        self._shop = None
        self._bill = None
        self._product = None
        self._dateTime = None
        self._date = None

    # серия практически одинаковых методов, немного поже сделаю тут фабрику, тобы не плодить одинаковый код
    def __addShop(self, bill):
        self._shop = self.session.query(Shops).filter_by(name=bill.shopName).filter_by(inn=bill.shopINN).filter_by(address=bill.retailAddr).first()
        if not self._shop:
            self._shop = Shops(bill.shopName, bill.shopINN, bill.retailAddr)
            self.session.add(self._shop)
            self.session.commit()

    def __addBill(self, bill):
        self._dateTime = datetime.datetime.fromtimestamp(bill.dateTime)
        self._date = self._dateTime.date()
        self._bill = self.session.query(Bills).filter_by(fiscalNum=bill.fiscalDocNum).filter_by(dateTime=self._dateTime).filter_by(shop=self._shop.id).filter_by(total=bill.total).first()
        if not self._bill:            
            self._bill = Bills(bill.fiscalDocNum, self._dateTime, self._shop.id, bill.total)
            self.session.add(self._bill)
            self.session.commit()

    def __addProduct(self, product:object):
        self._product = self.session.query(Products).filter_by(name=product.name).filter_by(shop=self._shop.id).filter_by(price=product.price).filter_by(date=self._date).first()
        if not self._product:
            self._product = Products(product.name, None, None, self._shop.id, product.price, self._date)
            self.session.add(self._product)
            self.session.commit()

    def __addPurchase(self, product:object):
        _purchase = self.session.query(Purchases).filter_by(product=self._product.id).filter_by(bill=self._bill.id).filter_by(quantity=product.quantity).filter_by(total=product.total).first()
        if not _purchase:
            _product = Purchases(self._product.id, self._bill.id, product.quantity, product.total)
            self.session.add(_product)
            self.session.commit()

    def parseBill(self, billsList: list):
        for bill in billsList:
            self.__addShop(bill)
            self.__addBill(bill)
            for product in bill.prodDataList:
                self.__addProduct(product)
                self.__addPurchase(product)

        print(self.session.query(Shops).all())
        print(self.session.query(Bills).all())
        print(self.session.query(Products).all())
        print(self.session.query(Purchases).all())

