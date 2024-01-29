# Flask app main file.

from flask import Flask, render_template, redirect, session, g, flash, request
from functools import wraps
from datetime import timedelta
import sys
import os

from helpers import common_helpers

print("\n-------------- species-challenge --------------\n", file = sys.stdout)

app = Flask(__name__)

# Get secret key from environment variables, stop if not found.
secret_key = os.environ.get("FLASK_SECRET_KEY")
if secret_key is None:
    raise ValueError("No FLASK_SECRET_KEY set.")
app.secret_key = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours = 2)

# ----------------------------------------
# Setup

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.is_admin:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user_data:
            flash("Kirjaudu ensin sisään.")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    # Make session permanent for all controllers
    session.permanent = True

    # Make user data available for controllers
    g.token = session.get("token", None)
    g.user_data = session.get("user_data", None)
    g.is_admin = session.get("is_admin", None)

# Make user data available for templates
@app.context_processor
def inject_user_data():
    return dict(user_data=g.user_data, is_admin=g.is_admin)

# ----------------------------------------
# Controllers

import controllers.index
@app.route("/")
def root():
    html = controllers.index.main()
    return render_template("index.html", html=html)


import controllers.admin
@app.route("/admin")
@admin_required
def admin():
    html = controllers.admin.main()
    return render_template("admin.html", html=html)


import controllers.participation
@app.route("/osallistuminen/<string:challenge_id_untrusted>", methods=['GET', 'POST'])
@app.route("/osallistuminen/<string:challenge_id_untrusted>/", methods=['GET', 'POST'])
@app.route("/osallistuminen/<string:challenge_id_untrusted>/<string:participation_id_untrusted>", methods=['GET', 'POST'])
@login_required
def new_participation(challenge_id_untrusted, participation_id_untrusted = None):
    if request.method == "GET":
        request.form = None
    html = controllers.participation.main(challenge_id_untrusted, participation_id_untrusted, request.form)

    if html.get('redirect'):
        return redirect(html['url'])
    
    return render_template("form_challenge100.html", html=html)


import controllers.challenge
@app.route("/admin/haaste", methods=['GET', 'POST'])
@app.route("/admin/haaste/", methods=['GET', 'POST'])
@app.route("/admin/haaste/<string:challenge_id_untrusted>", methods=['GET', 'POST'])
@admin_required
def challenge(challenge_id_untrusted = None):
    if request.method == "GET":
        request.form = None
    html = controllers.challenge.main(challenge_id_untrusted, request.form)

    if html.get('redirect'):
        return redirect(html['url'])
    
    return render_template("challenge.html", html=html)


@app.route("/login/<string:person_token_untrusted>")
def login(person_token_untrusted):
    person_token = common_helpers.clean_token(person_token_untrusted)

    # Get user data
    session["token"] = person_token
    session["user_data"] = common_helpers.fetch_finbif_api(f"https://api.laji.fi/v0/person/{ person_token }?access_token=")

    session["is_admin"] = False
    if ("MA.admin" in session["user_data"]["role"]):
        session["is_admin"] = True

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
