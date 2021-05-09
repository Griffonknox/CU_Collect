from .models import session, Acct_memb, Alert, Follow_Up, Acct_loans
import datetime

def query_account(clientkey, amount):
    if amount == 1:
        acct = session.query(Acct_memb).filter_by(varClientKey=clientkey).first()
        session.close()
    elif amount != 1:
        acct = session.query(Acct_memb).filter_by(varClientKey=clientkey).all()
        session.close()
    return acct

def query_loans(clientkey, amount):
    if amount == 1:
        acct = session.query(Acct_loans).filter_by(varClientKey=clientkey).first()
        session.close()
    elif amount != 1:
        acct = session.query(Acct_loans).filter_by(varClientKey=clientkey).all()
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


def create_account_(num, first, mid, last, address, city, state, zip, phone):
    new_acct = Acct_memb(varClientKey=num, first_name=first, middle_name=mid, last_name=last, phys_address=address, phys_city=city, phys_state=state, phys_zip=zip,phone=phone, phone2="", detail="", mail_address="", mail_city="", mail_state="", mail_zip="")
    session.add(new_acct)
    session.commit()
    session.close()


def create_follow(num, loan, detail, delq, user):
    last_id = session.query(Follow_Up).order_by(Follow_Up.key.desc()).first()
    session.close()
    last_id = int(last_id.key) + 1

    logged_user = user  #include logged in value
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert_create = Alert(key=last_id, varClientKey=num, Alert_Cat=cat, varEnteredBy=logged_user,
                              dateEntered=current_time, Alert_Detail=detail)

    session.add(alert_create)
    session.commit()
    session.close()


def create_loan_(num, loan_numb, acctnolnno, balance, user):
    last_id = session.query(Acct_loans).order_by(Acct_loans.key.desc()).first()
    session.close()
    last_id = int(last_id.key) + 1

    logged_user = user
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    loan_create = Acct_loans(key=last_id, varClientKey=num, loan_numb=loan_numb, varEnteredBy=logged_user,
                              dateEntered=current_time, acctnolnno=acctnolnno, balance=balance)

    session.add(loan_create)
    session.commit()
    session.close()


def edit_acct(num, first, middle, last, address, city, state, zip, m_address, m_city, m_state, m_zip, phone, phone2):
    acct = query_account(num, 1)
    acct.first_name = first
    acct.middle_name = middle
    acct.last_name = last
    acct.phys_address = address
    acct.phys_city = city
    acct.phys_state = state
    acct.phys_zip = zip
    acct.mail_address = m_address
    acct.mail_city = m_city
    acct.mail_state = m_state
    acct.mail_zip = m_zip
    acct.phone = phone
    acct.phone2 = phone2
    session.merge(acct)
    session.commit()
    session.close()
    return acct
