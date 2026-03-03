from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.db import Base

# --- כאן מתחילות המחלקות שלך (אל תמחק אותן!) ---

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    details = relationship("CustomerDetails", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class CustomerDetails(Base):
    __tablename__ = 'customer_details'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    shipping_address = Column(Text, nullable=False)
    phone_number = Column(String(20))

    user = relationship("User", back_populates="details")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)

    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default="Pending")

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")