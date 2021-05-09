from app import app, login_manager
from flask import render_template, redirect, url_for, request, flash
from .models import session, Follow_Up, Acct_memb, Alert, User, Acct_loans
from .utils import query_alert, query_account, query_follow, create_account_, edit_acct, create_follow, create_alert_, query_loans, create_loan_
from .config import verify_pass
from flask_login import login_user, login_required, current_user, logout_user
import pandas as pd


@app.route('/')
def log_in():
    return render_template("log_in.html")


@app.route("/authenticate", methods=["GET", "POST"])
def authenticate_user():
    user_name = request.form["username"]
    password = request.form["password"]

    # Locate user
    user = session.query(User).filter_by(username=user_name).first()
    session.close()

    if user and verify_pass(password, user.password):
        remember_me = False
        login_user(user, remember_me)
        return redirect(url_for("home"))
    else:
        flash('Incorrect User and/or Password. Please Try Again')
        return redirect(url_for("log_in"))




@app.route('/log_out')
@login_required
def log_out():
    logout_user()
    return redirect(url_for("log_in"))


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)



"""REPORTS SECTION"""

@app.route('/reports', methods=["GET", "POST"])
@login_required
def reports():
    return render_template("reports.html", user=current_user)


@app.route("/search_report", methods=['POST', 'GET'])
@login_required
def search_report():

    acct_num = request.form["acct_num"]

    acct_query = query_account(acct_num, 1)

    if acct_query:

        # PUll all follow ups and sort by date range
        date_from = request.form["from"]
        date_to = request.form["to"]

        follow_query = pd.read_sql(session.query(Follow_Up).filter_by(varClientKey=acct_num).statement, session.bind)
        session.close()

        follow_query["dt_"] = pd.to_datetime(follow_query["dateEntered"])
        mask = (follow_query["dt_"] > date_from) & (follow_query["dt_"] <= date_to)
        follow_query = follow_query.loc[mask]
        follow_query = follow_query.sort_values(by="dt_")
        del follow_query["dt_"]
        follow_query = follow_query.values.tolist()



        # query Alerts
        alert_query = query_alert(acct_num, 0, "client")  # consider to get descending
        if len(alert_query) != 0:
            return render_template("search_report.html", follow=follow_query, alerts="true", acct=acct_query,
                                   alert=alert_query[-1])
        else:
            return render_template("search_report.html", follow=follow_query, alerts="true", acct=acct_query)
    else:
        flash("No Accounts found.")
        return redirect(url_for("reports"))




"""ACCOUNT SECTION"""


@app.route("/search_account", methods=["POST", "GET"])
@login_required
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

        #query last 5 follow ups
        follow_recent = pd.read_sql(session.query(Follow_Up).filter_by(varClientKey=acct_num).statement, session.bind)
        session.close()
        follow_recent["dateEntered"] = pd.to_datetime(follow_recent['dateEntered'], dayfirst=True)
        follow_recent = follow_recent.sort_values('dateEntered', ascending=False)
        follow_recent = follow_recent.head(5)


        #Search Loan information
        acct_loans = query_loans(acct_num, 0)

        # query Alerts
        alert_query = query_alert(acct_num, 0, "client")  # consider to get descending
        if len(alert_query) != 0:
            flash("WARNING! ACCOUNT HAS ACTIVE ALERT(S)")
            return render_template("search_account.html", follow=follow_query, follow_recent=follow_recent.values.tolist(), alerts="true", acct=acct_query,
                                   alert=alert_query[-1], acct_loans= acct_loans)

        else:
            return render_template("search_account.html", follow=follow_query, follow_recent=follow_recent.values.tolist(), alerts="false", acct=acct_query, acct_loans=acct_loans)
    else:
        return render_template("no_account.html")


@app.route("/create_account", methods=["POST", "GET"])
@login_required
def create_account():
    # pull form template
    return render_template("create_account.html")


@app.route("/submit_account", methods=["POST", "GET"])
@login_required
def submit_account():
    account_num = request.form["account_num"]

    # see if existing account_num
    acct_query = query_account(account_num, 0)

    if len(acct_query) == 0:
        create_account_(account_num, request.form["first_name"], request.form["middle_name"],  request.form["last_name"],
                        request.form["phys_address"],request.form["phys_state"],request.form["phys_city"],request.form["phys_zip"], request.form["memb_phone"])

        flash("Account {} Successfully Made.".format(account_num))
        return redirect(url_for("home"))

    else:
        flash("Account Number {} Already in Use.".format(account_num))
        return redirect(url_for("home"))


@app.route("/edit_account", methods=["POST", "GET"])
@login_required
def edit_account():
    # query item, need to pull id number to query first
    acct_num = request.args.get('key')
    acct_query = query_account(acct_num, 1)
    return render_template("edit_account.html", acct=acct_query)


@app.route("/edit_acct_submit", methods=["POST", "GET"])
@login_required
def edit_acct_submit():
    # query item, need to pull id number to query first
    acct_query = edit_acct(request.form["account_num"], request.form["first_name"], request.form["middle_name"], request.form["last_name"], request.form["phys_address"],
                           request.form["phys_city"], request.form["phys_state"], request.form["phys_zip"], request.form["mail_address"],
                           request.form["mail_city"], request.form["mail_state"], request.form["mail_zip"],request.form["memb_phone"], request.form["memb_phone2"])  # edit acct and return

    return redirect(url_for("search_account", acct=acct_query.varClientKey))


@app.route("/update_acct_detail", methods=['POST', 'GET'])
@login_required
def update_acct_detail():
    acct_id = request.args.get("acct_id")
    acct_detail = request.form["acct_detail"]

    #update member existing data
    memb = session.query(Acct_memb).filter_by(varClientKey=acct_id).first()
    memb.detail = acct_detail
    session.merge(memb)
    session.commit()
    session.close()

    return "Member Detail Successfully Update"


"""ALL LOANS CATEGORIES"""
@app.route("/add_loan", methods=["GET", "POST"])
@login_required
def add_loan():
    acct_num = request.form["acct_num"]
    create_loan_(acct_num, request.form["loan_numb"], request.form["acctnolnno"], request.form["balance"], current_user.username)

    return redirect(url_for("search_account", acct=acct_num))




"""FOLLOW UP CATEGORIES"""
@app.route("/create_followup", methods=["POST", "GET"])
@login_required
def create_followup():
    # pull form template and pass acct_num
    acct_num = request.args.get('key')
    acct_loans = pd.read_sql(session.query(Acct_loans).filter_by(varClientKey=acct_num).statement, session.bind) # get loans of acct
    session.close()
    acct_loans = acct_loans["loan_numb"].unique()
    return render_template("create_followup.html", acct=acct_num, acct_loans=acct_loans)


@app.route("/view_followup", methods=["POST", "GET"])
@login_required
def view_followup():
    # pull form template
    follow_view = query_follow(request.args.get('key'), 1, "key")
    return render_template("view_followup.html", follow=follow_view)


@app.route("/followup_submit", methods=["POST", "GET"])
@login_required
def followup_submit():
    # add form data to DB
    create_follow(request.form["acct_num"], request.form["loan_num"],
                  request.form["editordata"], request.form["delq_days"], current_user.username)

    return redirect(url_for("search_account", acct=request.form["acct_num"]))




"""ALERT CATEGORIES"""
@app.route("/create_alert", methods=["POST", "GET"])
@login_required
def create_alert():
    acct_num = request.args.get('key')
    return render_template("create_alert.html", acct=acct_num)


@app.route("/view_alert", methods=["POST", "GET"])
@login_required
def view_alert():
    alert_view = query_alert(request.args.get('key'), 1, "key")
    return render_template("alert_view.html", alert=alert_view)


@app.route("/submit_alert", methods=["POST", "GET"])
@login_required
def submit_alert():
    create_alert_(request.form["key"], request.form["alert_cat"], request.form["editordata"], user=current_user.username)
    return redirect(url_for("search_account", acct=request.form["key"]))


# Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("Unauthorized User")
    return redirect(url_for("log_in"))


# @app.errorhandler(400)
# def access_forbidden(error):
#     flash(str(error.code) + " " + error.name)
#     return redirect(url_for("log_in"))


@app.errorhandler(403)
def access_forbidden(error):
    flash(str(error.code) + " " + error.name)
    return redirect(url_for("log_in"))


@app.errorhandler(404)
def not_found_error(error):
    flash(str(error.code) + " " + error.name)
    return redirect(url_for("log_in"))


@app.errorhandler(500)
def internal_error(error):
    flash(str(error.code) + " " + error.name)
    return redirect(url_for("log_in"))
