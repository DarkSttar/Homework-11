from sqlalchemy import Column,Integer,String,func,Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    emails = relationship("Email",backref='user')
    phone_numbers = relationship("PhoneNumber", backref='user')
    born_date = Column('born_date',DateTime)
    created_at = Column('created_at',DateTime,default=func.now())

class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer,primary_key=True)
    email = Column(String(100), nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey('users.id'))

class PhoneNumber(Base):
    __tablename__ = 'phonenumbers'
    id = Column(Integer,primary_key=True)
    number = Column(String(100), nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey('users.id'))