
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import REAL, TEXT


engine=create_engine('sqlite:///am.db')
Base=declarative_base()
Session=sessionmaker(bind=engine)
session=Session()

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
    city = Column(TEXT, nullable=False)
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
    grievance= Column(TEXT, nullable=False)

# def init_db():
#     Base.metadata.create_all(engine)
# def drop_db():
#     Base.metadata.drop_all(engine)
# drop_db()
# init_db()
# session.add_all([
#     User(name='test',mail='test@test.test',id_num='123123123'),
#     User(name='sha',mail='ysah18@student.oulu.fi',id_num='202181229'),
# ])
# session.add_all([
#     Plan(generation='3g',pay_method='prepaid',name='3G Prepaid',description='The only 3G Connection Plan.',price=10),
#     Plan(generation='4g',pay_method='prepaid',name='4G 100GB Prepaid',description='The most economical 4G plan which cost less than the postpaid one,',price=15),
#     Plan(generation='4g',pay_method='postpaid',name='4G 100GB Postpaid',description='4G Connect Plan with postpay.',price=20),
#     Plan(generation='4g',pay_method='prepaid',name='4G 200GB Postpaid',description='4G Connect Plan with prepay.',price=35),
#     Plan(generation='4g',pay_method='postpaid',name='4G 200GB Postpaid',description='4G Connect Plan with postpay.',price=40),
#     Plan(generation='4g',pay_method='postpaid',name='4G 400GB Postpaid',description='4G Connect Plan with prepay.',price=50),
#     Plan(generation='4g',pay_method='postpaid',name='4G 400GB Postpaid',description='4G Connect Plan with postpay.',price=55),
#     Plan(generation='5g',pay_method='prepaid',name='5G 200GB Postpaid',description='4G Connect Plan with prepay.',price=50),
#     Plan(generation='5g',pay_method='postpaid',name='5G 200GB Postpaid',description='4G Connect Plan with postpay.',price=55),
# ])
# session.add_all([
#     Shop(name='AM',city='oulu',location='XXXX, XXX',open_time='9:00',close_time='19:00'),
#     Shop(name='AM',city='nanjing',location='XXXX, XXX',open_time='9:00',close_time='19:00'),
# ])
# session.add_all([
#     SIM(user_id='123123123',plan_id=1,phone_num='123123123',status=1),
#     SIM(user_id='202181229',plan_id=2,phone_num='18901433999',status=1),
#     SIM(user_id='202181229',plan_id=3,phone_num='564125413',status=0),
# ])
# session.add_all([
#     Grievance(grievance='test'),
# ])
# session.commit()
for row in session.query(Plan).filter(Plan.generation == '4g').all():
    text = "Name:\t\t" + row.name + "\nGeneration:\t" + row.generation + "\nPay method:\t" + row.pay_method + "\nPrice:\t\t" + str(row.price) + '\nDescription:\t' + row.description + '\n'
    print(text)