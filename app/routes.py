from app import app
from flask import render_template, redirect, url_for, request, flash



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

    acct_num = request.form["acct_num"]
    print(acct_num)
    #query account  information by acct_number

    #query Alerts
    #if alerts then flash and do process
    flash("WARNING! ACCOUNT HAS ACTIVE ALERT(S)")

    #query all followups by account number
    data = list()
    for add in range(16):
        data.append(["3/27/2021", "Note", "UserAccountLoggedIN"])

    return render_template("search_account.html", data=data, alerts="true")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    #pull form template
    return render_template("create_account.html")

@app.route("/submit_account", methods=["POST", "GET"])
def submit_account():
    account_num = request.form["account_num"]
    memb_name = request.form["memb_name"]
    memb_address = request.form["memb_address"]
    print(account_num, memb_name, memb_address)
    return redirect(url_for("home"))


@app.route("/edit_account", methods=["POST", "GET"])
def edit_account():
    #query item, need to pull id number to query first
    acct_num = request.args.get('acct')
    print(acct_num)
    return render_template("edit_account.html", acct_num=acct_num)





"""FOLLOW UP CATEGORIES"""

@app.route("/create_followup", methods=["POST", "GET"])
def create_followup():
    #pull form template
    return render_template("create_followup.html")

@app.route("/view_followup", methods=["POST", "GET"])
def view_followup():
    #pull form template
    return render_template("view_followup.html")


@app.route("/followup_submit", methods=["POST", "GET"])
def followup_submit():
    # add form data to DB
    print(request.form["editordata"])
    print(request.form["call_type"])

    #requery table data
    return redirect(url_for("search_account"))





"""ALERT CATEGORIES"""

@app.route("/create_alert", methods=["POST", "GET"])
def create_alert():
    acct_num = request.args.get('acct')
    print(acct_num)
    return render_template("create_alert.html", acct_num=acct_num)
