from flask import Flask, render_template, redirect, session, g
import sys
import os

from helpers import common_helpers

import controllers.login

app = Flask(__name__)

# Get secret key from environment variables, stop if not found.
secret_key = os.environ.get('FLASK_SECRET_KEY')
if secret_key is None:
    raise ValueError("No FLASK_SECRET_KEY set.")
app.secret_key = secret_key

print("-------------- BEGIN --------------", file = sys.stdout)

# Make user data available for controllers
@app.before_request
def before_request():
    g.token = session.get('token', None)
    g.user_data = session.get('user_data', None)

# Make user data available for templates
@app.context_processor
def inject_user_data():
    return dict(user_data=g.user_data)

# ----------------------------------------
# Controllers

@app.route("/")
def root():
    html = controllers.index.main()
    return render_template("index.html", html=html)

@app.route("/login/<string:person_token_untrusted>")
def login(person_token_untrusted):
    # Get user data
    session['token'] = person_token_untrusted
    session['user_data'] = common_helpers.fetch_finbif_api(f"https://api.laji.fi/v0/person/{ person_token_untrusted }?access_token=")
    html = controllers.login.main(person_token_untrusted)
    return render_template("login.html", html=html)
