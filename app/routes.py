from app import app
from flask import render_template, redirect, url_for, request, flash
from .models import session, Follow_Up, Acct_memb, Alert
from .utils import query_alert, query_account, query_follow, create_account, edit_acct



@app.route('/')
def log_in():
    return render_template("log_in.html")


@app.route("/authenticate", methods=["GET", "POST"])
def authenticate_user():
    #check if log in information is correct to log in and push forward
    return redirect(url_for("home"))


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/log_out')
def log_out():
    return redirect(url_for("log_in"))




"""ACCOUNT CATEGORIES"""

@app.route("/search_account", methods=["POST", "GET"])
def search_account():

    if request.args.get('acct'):
        acct_num = request.args.get('acct')
    else:
        acct_num = request.form["acct_num"]

    #query account  information by acct_number
    acct_query = query_account(acct_num, 1)

    if acct_query:

        # query all followups by account number
        follow_query = query_follow(acct_num, 0)

        #query Alerts
        alert_query = query_alert(acct_num, 0)  # consider to get descending
        if len(alert_query) != 0:
            flash("WARNING! ACCOUNT HAS ACTIVE ALERT(S)")
            return render_template("search_account.html", follow=follow_query, alerts="true", acct=acct_query, alert=alert_query[0])

        else:
            return render_template("search_account.html", follow=follow_query, alerts="false", acct=acct_query)
    else:
        return render_template("no_account.html")



@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    #pull form template
    return render_template("create_account.html")

@app.route("/submit_account", methods=["POST", "GET"])
def submit_account():

    account_num = request.form["account_num"]
    memb_name = request.form["memb_name"]
    memb_address = request.form["memb_address"]

    if request.form["edit"]:  #accept edit request; return to search
        print(account_num, memb_name, memb_address)
        acct_query = edit_acct(account_num, memb_name, memb_address)  # edit acct and return
        return redirect(url_for("search_account", acct=acct_query.varClientKey))

    else:
        # see if existing account_num
        acct_query = query_account(account_num, 0)

        if len(acct_query) == 0:
            create_account(account_num, memb_name, memb_address)
            flash("Account {} Successfully Made.".format(account_num))
            return redirect(url_for("home"))

        else:
            flash("Account Number {} Already in Use.".format(account_num))
            return redirect(url_for("home"))


@app.route("/edit_account", methods=["POST", "GET"])
def edit_account():
    #query item, need to pull id number to query first
    acct_num = request.args.get('key')
    acct_query = query_account(acct_num, 1)
    return render_template("edit_account.html", acct=acct_query)





"""FOLLOW UP CATEGORIES"""

@app.route("/create_followup", methods=["POST", "GET"])
def create_followup():
    #pull form template and pass acct_num
    acct_num = request.args.get('key')
    return render_template("create_followup.html", acct=acct_num)

@app.route("/view_followup", methods=["POST", "GET"])
def view_followup():
    #pull form template
    follow_view = session.query(Follow_Up).filter_by(key=request.args.get('key')).first()
    return render_template("view_followup.html", follow=follow_view)


@app.route("/followup_submit", methods=["POST", "GET"])
def followup_submit():
    # add form data to DB
    print(request.form["editordata"])
    print(request.form["call_type"])
    print(request.form["acct_num"])

    follow_sub = Follow_Up(varClientKey=request.form["acct_num"], varCallType="test", varEnteredBy="test", datEnteredDatetime="test",
              txtDetails="test", varLoanNo=34)

    session.add(follow_sub)
    session.commit()
    session.close()
    #requery table data
    return redirect(url_for("search_account", acct=request.form["acct_num"]))





"""ALERT CATEGORIES"""

@app.route("/create_alert", methods=["POST", "GET"])
def create_alert():
    acct_num = request.args.get('key')
    return render_template("create_alert.html", alert=acct_num)

@app.route("/view_alert", methods=["POST", "GET"])
def view_alert():
    alert_view = session.query(Alert).filter_by(key=request.args.get('key')).first()
    return render_template("alert_view.html", alert=alert_view)