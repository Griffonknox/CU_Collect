import pandas as pd
import pymysql
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""CONNECT TO THE MYSQL DATABASE"""
username = "root"
password = "Password1!"
host = "192.168.1.245:3306"
dbname = "Collections"

url = "mysql+pymysql://{}:{}@{}/{}".format(username, password, host, dbname)
cnx = create_engine(url)
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
# df = pd.read_csv("NOTEPAD.TXT",sep="|")

def create_name(first, mid, last):
    if mid != mid:
        return "{} {}".format(first, last)
    else:
        return "{} {} {}".format(first, mid, last)



def add_accts():
    df_acct = pd.read_csv("Data/SWBC-MbExtract.csv")
    df_filter = df_acct[df_acct["Mb #"].isin([11690, 11652, 11741])]
    df_filter.columns = ["varClientKey", "first_name", "middle_name", "last_name", "address1", "address2", "address3", "city", "state", "zip"]
    print(df_filter.info())
    df_acct_load = pd.DataFrame()
    df_acct_load["varClientKey"] = df_filter["varClientKey"]
    df_acct_load["Acct_Name"] = df_filter.apply(lambda x: create_name(x.first_name, x.middle_name, x.last_name), axis=1)
    df_acct_load["Acct_Address"] = df_filter.apply(lambda x: "{} {} {} {}".format(x.address1, x.city, x.state, x.zip), axis=1)

    print(df_acct_load)
    dtype = {"varClientKey": Integer(), "Acct_name": String(100), "Acct_Address": String(150)}
    df_acct_load.to_sql('Memb_Account', if_exists='replace', con=cnx, chunksize=100, index=False, dtype=dtype)



def add_followup():
    df_follow = pd.read_csv("Data/FOLLOWUP.TXT", sep="|")
    df_filter = df_follow[df_follow["varClientKey"].isin([11690, 11652, 11741])]
    print(df_filter.info())
    del df_filter["varLoanKey"]
    df_filter["key"] = range(1, len(df_filter) + 1)


    dtype = {"key": Integer(), "varClientKey": Integer(), "dateEnteredDatetime": String(50), "varEnteredBy": String(100), "varCallType": String(50), "txtDetails": String(5000), "varLoanNo": Integer()}
    df_filter.to_sql('Follow_Up', if_exists='replace', con=cnx, chunksize=100, index=False, dtype=dtype)
    print(df_filter)




def add_alert():

    data = { "key": [1], "varClientKey": [11690], "Alert_Cat": ["Bankruptcy"], "varEnteredBy": ["UserTest"], "dateEntered": ["TestDate"], "Alert_Detail": ["Some test text here and there I want it to be big enought o show enough data room and what not of course"]}

    df_alert = pd.DataFrame(data, columns=["key", "varClientKey", "Alert_Cat", "varEnteredBy", "dateEntered", "Alert_Detail"])

    dtype = {"key": Integer(), "varClientKey": Integer(), "dateEntered": String(50), "varEnteredBy": String(100), "Alert_Cat": String(20), "Alert_Details": String(5000)}
    df_alert.to_sql('Alert', if_exists='replace', con=cnx, chunksize=100, index=False, dtype=dtype)

if __name__ == "__main__":
    # add_accts()
    # add_followup()
    add_alert()