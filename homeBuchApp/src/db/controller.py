from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, Float, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProductCategory(Base):
    __tablename__ = 'productcategory'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    comment = Column(String)

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return f'<ProductCategory({self.name}, {self.comment})>'

class ProductSubCategory(Base):
    __tablename__ = 'productsubcategory'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(Integer, ForeignKey('productcategory.id'))
    comment = Column(String)

    productcategory = relationship('ProductCategory', uselist=True,
                                   cascade='delete,all')

    def __init__(self, name, category, comment):
        self.name = name
        self.category = category
        self.comment = comment

    def __repr__(self):
        return f'<ProductSubCategory({self.category}, {self.name}, {self.comment})>'

class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    inn = Column(String)
    address = Column(String)
    comment = Column(String)

    def __init__(self, name, inn, address, comment):
        self.name = name
        self.inn = inn
        self.address = address
        self.comment = comment

    def __repr__(self):
        return f'<Shop({self.name}, {self.inn}, {self.address}, {self.comment})>'

class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True)
    fiscalNum = Column(String)
    dateTime = Column(DateTime)
    shop = Column(Integer, ForeignKey('shoprel.id'))
    total = Column(Float)
    comment = Column(String)

    shoprel = relationship('Shop', uselist=True, cascade='delete,all')

    def __init__(self, fiscalNum, dateTime, shop, total, comment):
        self.fiscalNum = fiscalNum
        self.dateTime = dateTime
        self.shop = shop
        self.total = total
        self.comment = comment

    def __repr__(self):
        return f'<Shop({self.fiscalNum}, {self.dateTime}, {self.shop}, {self.total}, {self.comment})>'

class Product(Base):
    __tablename__ = 'product'

    name = Column(String)
    category = Column(Integer, ForeignKey('cat.id'))
    subcategory = Column(Integer, ForeignKey('subcat.id'))
    comment = Column(String)
    shop = Column(Integer, ForeignKey('shoprel.id'))
    price = Column(Float)
    date = Column(Date)

    cat = relationship('ProductCategory', uselist=True, cascade='delete,all')
    subcat = relationship('ProductSubCategory', uselist=True, cascade='delete,all')
    shoprel = relationship('Shop', uselist=True, cascade='delete,all')

    def __init__(self, name, category, subcategory, shop, price, date, comment):
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

    product = Column(Integer, ForeignKey('prodrel.id'))
    bill = Column(Integer, ForeignKey('billrel.id'))
    comment = Column(String)
    quantity = Column(Float)
    total = Column(Float)

    prodrel = relationship('Product', uselist=True, cascade='delete,all')
    billrel = relationship('Bill', uselist=True, cascade='delete,all')

    def __init__(self, product, bill, quantity, total, comment):
        self.product = product
        self.bill = bill
        self.quantity = quantity
        self.total = total
        self.comment = comment

    def __repr__(self):
        return f'<Product({self.product}, {self.bill}, {self.quantity}, {self.comment})>'

class Controller():
    def __init__(self):
        self.db_engine = create_engine('sqlite:///server_db.db', \
            echo=False, pool_recycle=3600)
        Base.metadata.create_all(self.db_engine)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def parseBill(self, bill: object):
        pass
