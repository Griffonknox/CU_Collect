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
    last_id = session.query(Follow_Up).order_by(Follow_Up.key.desc()).first()
    session.close()
    last_id = int(last_id.key) + 1

    logged_user = user  #include logged in value
    current_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    follow_create = Follow_Up(key=last_id, varClientKey=num, varEnteredBy=logged_user, delq_days=delq,
                              dateEntered=current_time, txtDetails=detail, varLoanNo=loan)

    session.add(follow_create)
    session.commit()
    session.close()

def create_alert_(num, cat, detail, user):

    last_id = session.query(Follow_Up).order_by(Follow_Up.key.desc()).first()
    session.close()
    last_id = int(last_id.key) + 1


    logged_user = user
    current_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    alert_create = Alert(key=last_id, varClientKey=num, Alert_Cat=cat, varEnteredBy=logged_user,
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
