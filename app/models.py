from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), index=True)
    email: str = Column(String(50), unique=True, index=True)
    password: str = Column(String(50))


class Sale(Base):
    __tablename__ = "sales"

    id: int = Column(Integer, primary_key=True, index=True)
    total: int = Column(Integer)
    quantity: int = Column(Integer)
    product: str = Column(String)


class Product(Base):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, index=True)
    quantity: int = Column(Integer)
    name: str = Column(String)
    description: str = Column(String)


class Inventory(Base):
    __tablename__ = "inventory"

    id: int = Column(Integer, primary_key=True, index=True)
    product_name: int = Column(String)
    quantity: int = Column(Integer)
    warehouse: int = Column(Integer)


class DataWarehouse(Base):
    __tablename__ = "data_warehouse"

    id: int = Column(Integer, primary_key=True, index=True)
    data: dict = Column(JSON)
