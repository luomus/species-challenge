# Controller for a form to submit new participation to a challenge.
# Available for logged in users.

import datetime
from flask import g, flash
from helpers import common_db
from helpers import common_helpers

def insert_participation(challenge_id, form_data):
    """
    Validates the form data and inserts it into the database.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        bool: True if the form data was successfully validated and inserted, False otherwise.
    """
    # Validate form data
    if not form_data["participant_name"]:
        flash("Osallistujan nimi puuttuu.")
        return False
    if not form_data["location"]:
        flash("Paikka puuttuu.")
        return False

    # Current datetime in MySQL format
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert form data into the database
    params = (
        challenge_id,
        form_data["participant_name"],
        form_data["location"],
        g.user_data["id"],
        now,
        g.user_data["id"],
        now
    )

    with common_db.connection() as conn:
        query = "INSERT INTO participations (challenge_id, participant_name, location, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        success = common_db.insert(conn, query, params)

    return success


def main(challenge_id_untrusted, form_data = None):
    html = dict()

    challenge_id = common_helpers.clean_uuid(challenge_id_untrusted)

    # Check that challenge exists and is open
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE id = %s AND status = 'open'"
        params = (challenge_id,)
        challenge = common_db.select(conn, query, params)

    print(challenge)

    if not challenge:
        flash("Haastetta ei löytynyt tai siihen ei voi enää osallistua.")
        return html
    
    challenge_id = challenge[0]["id"]
    html["challenge_id"] = challenge_id
    html["challenge_name"] = challenge[0]["name"]

    # If user already submitted data, use that to fill in the form.
    if form_data:
        if insert_participation(challenge_id, form_data):
            flash("Osallistumisesi on nyt tallennettu.")
        else:
            flash("Tarkista lomakkeen tiedot ja yritä uudelleen.")

    # If no form_data, show an empty form for a new submission.
    else:
        print("Empty form")

    print(g.token)
    print(g.user_data)

    return html