from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, create_engine, Integer, Date, ForeignKey, func, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship

from ..utils.config import settings

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    city = Column(String, nullable=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


# Products Table
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String, nullable=True) # bucket_aws, bucket_oci
    stock = Column(Integer, nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.id'))

    brand = relationship('Brand', back_populates='products')
    cart_items = relationship('Cart', back_populates='product')
    sale_details = relationship('SaleDetail', back_populates='product')


# Brands Table
class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    products = relationship('Product', back_populates='brand')


# Cart Table
class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    date_added = Column(DateTime, server_default=func.now())

    user = relationship('User', back_populates='cart_items')
    product = relationship('Product', back_populates='cart_items')


# Sales Table
class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, server_default=func.now())
    total = Column(DECIMAL(10, 2), nullable=False)

    # envio de correo

    user = relationship('User', back_populates='sales')
    sale_details = relationship('SaleDetail', back_populates='sale')


# Sale Details Table
class SaleDetail(Base):
    __tablename__ = 'sale_details'

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)

    sale = relationship('Sale', back_populates='sale_details')
    product = relationship('Product', back_populates='sale_details')


SQLALCHEMY_DATABASE_URL = settings.db_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)