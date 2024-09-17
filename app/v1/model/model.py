from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, create_engine, Integer, Date, ForeignKey, func, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship

#from app.v1.utils.config import settings

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    username = Column(String, unique=True)
    role = Column(String(50), nullable=False, default="user")
    hashed_password = Column(String)


    sales = relationship('Sale', back_populates='user')
    cart_items = relationship('Cart', back_populates='user')


# Products Table
class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String, nullable=True) # bucket_aws, bucket_oci
    stock = Column(Integer, nullable=False)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'))

    brand = relationship('Brand', back_populates='products')
    cart_items = relationship('Cart', back_populates='product')
    sale_details = relationship('SaleDetail', back_populates='product')


# Brands Table
class Brand(Base):
    __tablename__ = 'brands'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    products = relationship('Product', back_populates='brand')


# Cart Table
class Cart(Base):
    __tablename__ = 'cart'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    date_added = Column(DateTime, server_default=func.now())

    user = relationship('User', back_populates='cart_items')
    product = relationship('Product', back_populates='cart_items')


# Sales Table
class Sale(Base):
    __tablename__ = 'sales'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    date = Column(DateTime, server_default=func.now())
    total = Column(DECIMAL(10, 2), nullable=False)

    # envio de correo

    user = relationship('User', back_populates='sales')
    sale_details = relationship('SaleDetail', back_populates='sale')

    def calculate_total(self):
        total = 0
        for sale_detail in self.sale_details:
            total += sale_detail.quantity * sale_detail.price
        self.total = total


# Sale Details Table
class SaleDetail(Base):
    __tablename__ = 'sale_details'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    sale_id = Column(UUID(as_uuid=True), ForeignKey('sales.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)

    sale = relationship('Sale', back_populates='sale_details')
    product = relationship('Product', back_populates='sale_details')


#SQLALCHEMY_DATABASE_URL = settings.db_url
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5433/figures_store'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)