import pymysql
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import SQLALCHEMY_DATABASE_URL



cnx = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = sessionmaker()
db_session.configure(bind=cnx)
session = db_session()
Base = declarative_base(db_session)


class Acct_memb(Base):
    __tablename__ = "Memb_Account"
    varClientKey = Column(Integer(), primary_key=True)
    Acct_Name = Column(String(50))
    Acct_Address = Column(String(150))


class Alert(Base):
    __tablename__ = "Alert"
    key = Column(Integer(), primary_key=True)
    varClientKey = Column(Integer())
    Alert_Cat = Column(String(20))
    varEnteredBy = Column(String(100))
    dateEntered = Column(String(50))
    Alert_Detail = Column(String(5000))


class Follow_Up(Base):
    __tablename__ = "Follow_Up"
    key = Column(Integer(), primary_key=True)
    varClientKey = Column(Integer())
    varCallType = Column(String(50))
    varEnteredBy = Column(String(100))
    datEnteredDatetime = Column(String(50))
    txtDetails = Column(String(5000))
    varLoanNo = Column(Integer)

