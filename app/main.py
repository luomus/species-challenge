# Flask app main file.

from flask import Flask, render_template, redirect, session, g, flash
from functools import wraps
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

# Make user data available for controllers
@app.before_request
def before_request():
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


import controllers.new_participation
@app.route("/uusi_osallistuminen")
@login_required
def new_participation():
    html = controllers.new_participation.main()
    return render_template("new_participation.html", html=html)


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
