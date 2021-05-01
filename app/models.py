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
    varClientKey = Column(Integer(), primary_key=True)
    acct_name = Column(String(50))
    acct_address = Column(String(150))
    acct_address2 = Column(String(150))
    phone = Column(String(20))
    phone2 = Column(String(20))
    detail = Column(String(1000))



class Alert(Base):
    __tablename__ = "alert"
    key = Column(Integer(), primary_key=True)
    varClientKey = Column(Integer())
    Alert_Cat = Column(String(20))
    varEnteredBy = Column(String(100))
    dateEntered = Column(String(50))
    Alert_Detail = Column(String(5000))


class Follow_Up(Base):
    __tablename__ = "follow_up"
    key = Column(Integer(), primary_key=True)
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
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    password = Column(String(30))
    urole = Column(Integer)
    full_name = Column(String(150))


