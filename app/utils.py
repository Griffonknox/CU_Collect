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


def query_alert(key, amount, search):
    if search == "key":
        if amount == 1:
            alert = session.query(Alert).filter_by(key=key).first()
            session.close()
        elif amount != 1:
            alert = session.query(Alert).filter_by(key=key).all()
            session.close()
        return alert
    elif search == "client":
        if amount == 1:
            alert = session.query(Alert).filter_by(varClientKey=key).first()
            session.close()
        elif amount != 1:
            alert = session.query(Alert).filter_by(varClientKey=key).all()
            session.close()
        return alert


def query_follow(key, amount, search):
    if search == "key":
        if amount == 1:
            follow = session.query(Follow_Up).filter_by(key=key).first()
            session.close()
        elif amount != 1:
            follow = session.query(Follow_Up).filter_by(key=key).all()
            session.close()
        return follow
    elif search == "client":
        if amount == 1:
            follow = session.query(Follow_Up).filter_by(varClientKey=key).first()
            session.close()
        elif amount != 1:
            follow = session.query(Follow_Up).filter_by(varClientKey=key).all()
            session.close()
        return follow


def create_account_(num, name, address, phone):
    new_acct = Acct_memb(varClientKey=num, acct_name=name, acct_address=address, phone=phone)
    session.add(new_acct)
    session.commit()
    session.close()


def create_follow(num, loan, detail, delq, user):
    print(num, loan, detail, delq, user)

    logged_user = user  #include logged in value
    current_time = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

    follow_create = Follow_Up(varClientKey=num, varEnteredBy=logged_user, delq_days=delq,
                              dateEntered=current_time, txtDetails=detail, varLoanNo=loan)

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



def edit_acct(num, name, address, address2, phone, phone2):
    acct = query_account(num, 1)
    acct.acct_name = name
    acct.acct_address = address
    acct.acct_address2 = address2
    acct.phone = phone
    acct.phone2 = phone2
    session.merge(acct)
    session.commit()
    session.close()
    return acct
