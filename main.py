import pandas as pd
import pymysql
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""CONNECT TO THE MYSQL DATABASE"""
# username = "root"
# password = "Password1!"

# dbname = "Collections"

# url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, host, dbname)
# cnx = create_engine(url)
# df = pd.read_sql('SELECT varClientKey FROM Follow_Up', cnx)  # read the entire table

# df = pd.DataFrame(columns = ["varClientKey", "datEnteredDatetime", "varEnteredBy", "varCallType", "txtDetails", "varLoanNo"])

# print(len(df["varClientKey"].unique()))

"""IMPORT THE FOLLOWUP DATA"""

# df = pd.read_csv("FOLLOWUP.TXT",sep="|")
#
# print(df.info())
# del df["varLoanKey"]
# df["datEnteredDatetime"] = pd.to_datetime(df["datEnteredDatetime"], format='%d%b%Y:%H:%M:%S.%f')
#
#
#
# row = df.iloc[39]
# print(row["txtDetails"])
# print(row["datEnteredDatetime"])
#
# df.to_sql('Follow_Up', if_exists='replace', con=cnx, chunksize=100, index=False, dtype={"varClientKey": Integer(), "datEnteredDatetime": String(50), "varEnteredBy": String(50), "varCallType": String(50), "txtDetails": String(), "varLoanNo": String(50)})


"""CHECKING OUT NOTEPAD DATA"""
df = pd.read_csv("NOTEPAD.TXT",sep="|")


print(df.info())
filtered_df = df[df['txtNotepad'].notnull()]
print(filtered_df.info())

"""CHECKING OUT SQLALCHEMY"""
username = "root"
password = "Password1!"

dbname = "Collections"

url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, host, dbname)
cnx = create_engine(url)
db_session = sessionmaker()
db_session.configure(bind=cnx)
session = db_session()
Base = declarative_base(db_session)

class Follow_Up(Base):
    __tablename__ = "Follow_Up"
    id = Column(Integer(), primary_key=True)
    varClientKey = Column(Integer())
    varCallType = Column(String(50))



query = session.query(Follow_Up).filter_by(varClientKey=167723).all()

print(len(query))
for item in query:
    print(item.varCallType)
