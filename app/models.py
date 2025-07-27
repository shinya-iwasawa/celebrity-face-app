from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String, index=True)
    address = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    mobile_phone = Column(String)
