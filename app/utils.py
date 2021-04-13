from .models import session, Acct_memb, Alert, Follow_Up
import datetime

def query_account(clientkey, amount):
    if amount == 1:
        acct = session.query(Acct_memb).filter_by(varClientKey=clientkey).first()
        session.close()
    elif amount != 1:
        acct = session.query(Acct_memb).filter_by(varClientKey=clientkey).all()
        session.close()
    return acct


def query_alert(clientkey, amount):
    if amount == 1:
        alert = session.query(Alert).filter_by(varClientKey=clientkey).first()
        session.close()
    elif amount != 1:
        alert = session.query(Alert).filter_by(varClientKey=clientkey).all()
        session.close()
    return alert


def query_follow(clientkey, amount):
    if amount == 1:
        follow = session.query(Follow_Up).filter_by(varClientKey=clientkey).first()
        session.close()
    elif amount != 1:
        follow = session.query(Follow_Up).filter_by(varClientKey=clientkey).all()
        session.close()
    return follow


def create_account(num, name, address):
    new_acct = Acct_memb(varClientKey=num, Acct_Name=name, Acct_Address=address)
    session.add(new_acct)
    session.commit()
    session.close()


def create_follow(num, call, loan, detail):

    logged_user = "tst"  #include logged in value
    current_time = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

    follow_create = Follow_Up(varClientKey=num, varCallType=call, varEnteredBy=logged_user,
                              datEnteredDatetime=current_time, txtDetails=detail, varLoanNo=loan)

    session.add(follow_create)
    session.commit()
    session.close()

def create_alert_(num, cat, detail):
    logged_user = "tst"  # include logged in value
    current_time = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

    alert_create = Alert(varClientKey=num, Alert_Cat=cat, varEnteredBy=logged_user,
                              dateEntered=current_time, Alert_Detail=detail)

    session.add(alert_create)
    session.commit()
    session.close()



def edit_acct(num, name, address):
    acct = query_account(num, 1)
    acct.Acct_Name = name
    acct.Acct_Address = address
    session.merge(acct)
    session.commit()
    session.close()
    return acct
