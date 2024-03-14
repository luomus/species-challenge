# Flask app main file.

from flask import Flask, render_template, redirect, session, g, flash, request, send_from_directory
from functools import wraps
from datetime import timedelta
import sys
import os
import requests

from helpers import common_helpers
from helpers.common_db import DatabaseConnectionError


print("\n-------------- species-challenge --------------\n", file = sys.stdout)

app = Flask(__name__)

# Get secret key from environment variables, stop if not found.
secret_key = os.environ.get("FLASK_SECRET_KEY")
if secret_key is None:
    raise ValueError("No FLASK_SECRET_KEY set.")
app.secret_key = secret_key

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 10)

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
            flash("<a href='/login'>Kirjaudu ensin sisään</a>.")
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

@app.errorhandler(DatabaseConnectionError)
def handle_db_connection_error(error):
    return "<h3>Huoltokatko</h3><p>Palvelussa on katko joka kuukauden ensimmäinen torstai klo 8-10. Muista katkoista pyritään tiedottamaan <a href='https://laji.fi/'>Laji.fi-portaalissa</a>.</p> {}".format(error), 502

@app.errorhandler(500)
def internal_error(error):
    return "<h3>Anteeksi, tapahtui virhe!</h3><p>Palaa takaisin selaimen takaisin/back -nappia painamalla.</p> {}".format(error), 500

# ----------------------------------------
# Controllers

import controllers.index
@app.route("/")
def root():
    html = controllers.index.main()
    return render_template("index.html", html=html)


import controllers.my
@app.route("/oma")
@login_required
def my():
    html = controllers.my.main()
    return render_template("my.html", html=html)


import controllers.challenge
@app.route("/haaste/<string:challenge_id_untrusted>")
@app.route("/haaste/<string:challenge_id_untrusted>/")
def challenge(challenge_id_untrusted):
    html = controllers.challenge.main(challenge_id_untrusted)

    if html.get('redirect'):
        return redirect(html['url'])

    return render_template("challenge.html", html=html)


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


import controllers.participation_stats
@app.route("/tilasto/<string:challenge_id_untrusted>/<string:participation_id_untrusted>")
@login_required
def participation_stats(challenge_id_untrusted, participation_id_untrusted):
    html = controllers.participation_stats.main(challenge_id_untrusted, participation_id_untrusted)

    if html.get('redirect'):
        return redirect(html['url'])

    return render_template("participation_stats.html", html=html)


import controllers.admin_challenge
@app.route("/admin/haaste", methods=['GET', 'POST'])
@app.route("/admin/haaste/", methods=['GET', 'POST'])
@app.route("/admin/haaste/<string:challenge_id_untrusted>", methods=['GET', 'POST'])
@admin_required
def admin_challenge(challenge_id_untrusted = None):
    if request.method == "GET":
        request.form = None
    html = controllers.admin_challenge.main(challenge_id_untrusted, request.form)

    if html.get('redirect'):
        return redirect(html['url'])
    
    return render_template("admin_challenge.html", html=html)

'''
import controllers.admin_contacts
@app.route("/admin/yhteys/<string:challenge_id_untrusted>")
@admin_required
def admin_contacts(challenge_id_untrusted = None):
    html = controllers.admin_contacts.main(challenge_id_untrusted)
    return render_template("admin_contacts.html", html=html)
'''

@app.route("/login")
def login_page():
    person_token_untrusted = request.args.get('token', None)

    itsystem_id = os.environ.get("ITSYSTEM")
    # Localhost
    if "KE.1521" == itsystem_id:
        login_url = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/login?target=KE.1521&redirectMethod=GET&locale=fi&next="
        api_url = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/token/"
    # Dev/staging
    elif "KE.1522" == itsystem_id:
        login_url = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/login?target=KE.1522&redirectMethod=GET&locale=fi&next="
        api_url = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/token/"
    # Production
    elif "KE.1741" == itsystem_id:
        login_url = "https://login.laji.fi/login?target=KE.1741&redirectMethod=GET&locale=fi&next="
        api_url = "https://login.laji.fi/laji-auth/token/"

    # Case A: User is logging in
    if person_token_untrusted:
        print("LOGGING IN...")

        session.clear() # Clear any previous session data
        person_token = common_helpers.clean_token(person_token_untrusted)

        # Get user data
        user_data_from_api = common_helpers.fetch_lajiauth_api(api_url + person_token)
        print("USER DATA: ", user_data_from_api)
        '''
        User data is in this format:
        {
        'user': {
            'authSourceId': 'testaaja@example.fi', 
            'qname': 'MA.123...', 
            'yearOfBirth': 2000, 
            'firstJoined': None, 
            'preferredName': 'Teppo', 
            'inheritedName': 'Testaaja', 
            'name': 'Teppo Testaaja', 
            'email': 'testaaja@example.fi', 
            'defaultLanguage': None, 
            'group': None, 
            'roles': [
                'MA.speciesChallengeAdmin'
            ],
            'organisations': [],
            'previousEmailAddresses': [],
            'additionalUserIds': {'VANHA_HATIKKA': ['testaaja']},
            'address': None
        },
        'source': 'LOCAL',
        'target': 'KE.1521',
        'next': '',
        'redirectMethod': 'GET',
        'permanent': False
    }
        '''

        # Case A1: Login failed
        if "code" in user_data_from_api:
            print("LOGIN ERROR: ", user_data_from_api)
            flash("Kirjautuminen epäonnistui. Yritä uudelleen.")
            return redirect("/login")

        # Case A2: Login successful        
        session["token"] = person_token
        session["user_data"] = dict()
        session["user_data"]["id"] = user_data_from_api["user"]["qname"]
        session["user_data"]["fullName"] = user_data_from_api["user"]["name"]

        session["is_admin"] = False # default
        if "roles" in user_data_from_api['user']:
            if "MA.speciesChallengeAdmin" in user_data_from_api['user']["roles"]:
                session["is_admin"] = True

        print("IS ADMIN: ", session["is_admin"])
        return redirect("/")
    
    # Case B: User already logged in
    if g.user_data:
        print(g.user_data)
        flash(f"Olet jo kirjautunut sisään nimellä { g.user_data.get('fullName', '(tunnukseesi ei ole kirjattu nimeä)') }.", "info")
        return redirect("/")
    
    # Case C: User not logged in, show login instructions
    else:
        return render_template("login.html", login_url=login_url)


@app.route("/logout")
def logout():
    session.clear()

    itsystem_id = os.environ.get("ITSYSTEM")
    # Localhost
    if "KE.1521" == itsystem_id:
        api_url = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/token/"
    # Dev/staging
    elif "KE.1522" == itsystem_id:
        api_url = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/token/"
    # Production
    elif "KE.1741" == itsystem_id:
        api_url = "https://login.laji.fi/laji-auth/token/"

    url = api_url + g.token
    response = requests.delete(url)

    # Checking if the request was successful
    if response.status_code == 200:
        flash("Olet kirjautunut ulos.", "info")
        return redirect("/")
    else:
        print('Failed to delete session on Laji-auth.')
        print('Status code:', response.status_code)
        print('Response:', response.text)
        flash("Tietokantavirhe, uloskirjautuminen epäonnistui.", "error")
        return redirect("/")


import controllers.health
@app.route("/health/database")
def health_database():
    errors = controllers.health.main()
    if errors:
        return errors, 500
    else:
        return "OK", 200


@app.route("/health")
def health():
    return "OK", 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

