import pymysql
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import SQLALCHEMY_DATABASE_URL
from flask_login import UserMixin
from app import login_manager

cnx = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = sessionmaker()
db_session.configure(bind=cnx)
session = db_session()
Base = declarative_base(db_session)


class Acct_memb(Base):
    __tablename__ = "memb_account"
    varClientKey = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))

    phys_address = Column(String(50))
    phys_city = Column(String(50))
    phys_state = Column(String(50))
    phys_zip = Column(String(50))

    mail_address = Column(String(50))
    mail_city = Column(String(50))
    mail_state = Column(String(50))
    mail_zip = Column(String(50))

    phone = Column(String(20))
    phone2 = Column(String(20))
    detail = Column(String(1000))

class Acct_loans(Base):
    __tablename__ = "acct_loans"
    key = Column(Integer(), primary_key=True, autoincrement=True)
    varClientKey = Column(Integer())
    loan_numb = Column(String(25))
    acctnolnno = Column(Integer())
    balance = Column(String(20))
    varEnteredBy = Column(String(100))
    dateEntered = Column(String(50))


class Alert(Base):
    __tablename__ = "alert"
    key = Column(Integer(), primary_key=True, autoincrement=True)
    varClientKey = Column(Integer())
    Alert_Cat = Column(String(20))
    varEnteredBy = Column(String(100))
    dateEntered = Column(String(50))
    Alert_Detail = Column(String(5000))


class Follow_Up(Base):
    __tablename__ = "follow_up"
    key = Column(Integer(), primary_key=True, autoincrement=True)
    varClientKey = Column(Integer())
    varEnteredBy = Column(String(100))
    dateEntered = Column(String(50))
    txtDetails = Column(String(5000))
    varLoanNo = Column(String(25))
    delq_days = Column(String(20))



@login_manager.user_loader
def get_user(userid):
    user = session.query(User).filter_by(id=userid).first()
    session.close()
    return user



class User(Base, UserMixin):
    __tablename__ = "usr"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    password = Column(String(30))
    urole = Column(Integer)
    full_name = Column(String(150))


