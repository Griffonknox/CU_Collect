from app import app
from flask import render_template, redirect, url_for, request, flash
from .models import session, Follow_Up, Acct_memb, Alert
from .utils import query_alert, query_account, query_follow, create_account_, edit_acct, create_follow, create_alert_


@app.route('/')
def log_in():
    return render_template("log_in.html")


@app.route("/authenticate", methods=["GET", "POST"])
def authenticate_user():
    # check if log in information is correct to log in and push forward
    return redirect(url_for("home"))


@app.route('/log_out')
def log_out():
    return redirect(url_for("log_in"))


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/reports')
def reports():
    return render_template("reports.html")


@app.route("/search_report", methods=['POST', 'GET'])
def search_report():

    acct_num = request.form["acct_num"]

    acct_query = query_account(acct_num, 1)

    if acct_query:

        # query all followups by account number
        follow_query = query_follow(acct_num, 0, "client")

        # apply date filter
        # date_from = request.form["from"]
        # date_to = request.form["to"]

        # query Alerts
        alert_query = query_alert(acct_num, 0, "client")  # consider to get descending
        if len(alert_query) != 0:
            return render_template("search_report.html", follow=follow_query, alerts="true", acct=acct_query,
                                   alert=alert_query[-1])
        else:
            return render_template("search_report.html", follow=follow_query, alerts="true", acct=acct_query,
                                   alert=alert_query[-1])
    else:
        flash("No Accounts found.")
        return redirect(url_for("reports"))




"""ACCOUNT CATEGORIES"""


@app.route("/search_account", methods=["POST", "GET"])
def search_account():
    if request.args.get('acct'):
        acct_num = request.args.get('acct')
    else:
        acct_num = request.form["acct_num"]

    # query account  information by acct_number
    acct_query = query_account(acct_num, 1)

    if acct_query:

        # query all followups by account number
        follow_query = query_follow(acct_num, 0, "client")

        # query Alerts
        alert_query = query_alert(acct_num, 0, "client")  # consider to get descending
        if len(alert_query) != 0:
            flash("WARNING! ACCOUNT HAS ACTIVE ALERT(S)")
            return render_template("search_account.html", follow=follow_query, alerts="true", acct=acct_query,
                                   alert=alert_query[-1])

        else:
            return render_template("search_account.html", follow=follow_query, alerts="false", acct=acct_query)
    else:
        return render_template("no_account.html")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    # pull form template
    return render_template("create_account.html")


@app.route("/submit_account", methods=["POST", "GET"])
def submit_account():
    account_num = request.form["account_num"]

    # see if existing account_num
    acct_query = query_account(account_num, 0)

    if len(acct_query) == 0:
        create_account_(account_num, request.form["memb_name"], request.form["memb_address"])
        flash("Account {} Successfully Made.".format(account_num))
        return redirect(url_for("home"))

    else:
        flash("Account Number {} Already in Use.".format(account_num))
        return redirect(url_for("home"))


@app.route("/edit_account", methods=["POST", "GET"])
def edit_account():
    # query item, need to pull id number to query first
    acct_num = request.args.get('key')
    acct_query = query_account(acct_num, 1)
    return render_template("edit_account.html", acct=acct_query)


@app.route("/edit_acct_submit", methods=["POST", "GET"])
def edit_acct_submit():
    # query item, need to pull id number to query first
    acct_query = edit_acct(request.form["account_num"], request.form["memb_name"],
                           request.form["memb_address"])  # edit acct and return
    return redirect(url_for("search_account", acct=acct_query.varClientKey))


"""FOLLOW UP CATEGORIES"""
@app.route("/create_followup", methods=["POST", "GET"])
def create_followup():
    # pull form template and pass acct_num
    acct_num = request.args.get('key')
    return render_template("create_followup.html", acct=acct_num)


@app.route("/view_followup", methods=["POST", "GET"])
def view_followup():
    # pull form template
    follow_view = query_follow(request.args.get('key'), 1, "key")
    return render_template("view_followup.html", follow=follow_view)


@app.route("/followup_submit", methods=["POST", "GET"])
def followup_submit():
    # add form data to DB
    create_follow(request.form["acct_num"], request.form["call_type"], request.form["loan_num"],
                  request.form["editordata"])

    return redirect(url_for("search_account", acct=request.form["acct_num"]))




"""ALERT CATEGORIES"""
@app.route("/create_alert", methods=["POST", "GET"])
def create_alert():
    acct_num = request.args.get('key')
    return render_template("create_alert.html", acct=acct_num)


@app.route("/view_alert", methods=["POST", "GET"])
def view_alert():
    alert_view = query_alert(request.args.get('key'), 1, "key")
    return render_template("alert_view.html", alert=alert_view)


@app.route("/submit_alert", methods=["POST", "GET"])
def submit_alert():
    create_alert_(request.form["key"], request.form["alert_cat"], request.form["editordata"])
    return redirect(url_for("search_account", acct=request.form["key"]))
