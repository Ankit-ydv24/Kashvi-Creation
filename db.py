from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True)
    customer_name = Column(String(30), nullable=False)
    description = Column(String(500))
    visibility_on_homepage = Column(Boolean, default=False)
    
    

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    product_image = Column(String(255))
    variety = Column(String(20))
    selling_price = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(500))
    
    # Relationships
    invoice_items = relationship('InvoiceItem', back_populates='product')
  

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    city = Column(String(50),  nullable=False)
    state = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    zip = Column(String(100), nullable=False)
    
    # Relationships

    invoices = relationship('Invoice', back_populates='customer')
  


    

class Invoice(Base):
    __tablename__ = 'invoices'
    
    invoice_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    customer = relationship('Customer', back_populates='invoices')
    invoice_items = relationship('InvoiceItem', back_populates='invoice')

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    
    invoice_item_id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.invoice_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    invoice = relationship('Invoice', back_populates='invoice_items')
    product = relationship('Product', back_populates='invoice_items')


def init_db():
    # Replace with your actual database URL
    engine = create_engine('sqlite:///ecommerce.db', echo=True)
    Base.metadata.create_all(engine)
    return engine

if __name__ == '__main__':
    init_db()