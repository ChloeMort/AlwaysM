
from sqlalchemy import Column, Integer, REAL
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TEXT, Boolean, Float


Base = declarative_base()

class User(Base):

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)
    mail = Column(TEXT, nullable=False)
    id_num = Column(TEXT, nullable=False, unique=True)


class Plan(Base):

    __tablename__ = "plan"
    id = Column(Integer, primary_key=True, nullable=False)
    generation = Column(TEXT, nullable=False)
    pay_method = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
    price = Column(REAL, nullable=False)


class Shop(Base):

    __tablename__ = "shop"
    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)
    location = Column(TEXT, nullable=False)
    open_time = Column(TEXT, nullable=False)
    close_time = Column(TEXT, nullable=False)


class SIM(Base):

    __tablename__ = "sim"
    id = Column(Integer, primary_key=True)
    user_id = Column(TEXT, ForeignKey(User.id_num), nullable=False)
    plan_id = Column(Integer, ForeignKey(Plan.id), nullable=False)
    phone_num = Column(TEXT, nullable=False)
    status = Column(Integer, nullable=False)


class Grievance(Base):

    __tablename__ = "grievance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    grievance= Column(TEXT, nullable=False)


