# Controller for a form to submit new participation to a challenge.
# Available for logged in users.

import datetime
from flask import g, flash, redirect
from helpers import common_db
from helpers import common_helpers

def insert_participation(challenge_id, form_data):
    """
    Inserts participation data to the database.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        bool: True if the form data was successfully validated and inserted, False otherwise.
    """

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


def validate_data(form_data):
    """
    Validates the form data.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        string: A validation error message, or empty if no errors were found.
    """
    errors = ""

    # Validate form data
    if not form_data["name"]:
        errors += "Osallistujan nimi puuttuu."
    if not form_data["location"]:
        errors += "Paikka puuttuu."

    return errors



def main(challenge_id_untrusted, participation_id_untrusted, form_data = None):
    html = dict()

    challenge_id = common_helpers.clean_uuid(challenge_id_untrusted)
    participation_id = common_helpers.clean_uuid(participation_id_untrusted)
    html["challenge_id"] = challenge_id
    html["participation_id"] = participation_id

    # Todo: Check if this is needed
    if html["participation_id"] == None:
        html["participation_id"] = ""

    # Check that challenge exists and is open
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE id = %s AND status = 'open'"
        params = (challenge_id,)
        challenge = common_db.select(conn, query, params)

    if not challenge:
        flash("Haastetta ei löytynyt tai siihen ei voi enää osallistua.")
        return redirect("/")

    # Get challenge information
    print(challenge) # Debug
    html["challenge_name"] = challenge[0]["name"]

    # Case A: User opened an existing participation for editing.
    if participation_id and not form_data:
        # Load participation data from the database
        with common_db.connection() as conn:
            query = "SELECT * FROM participations WHERE id = %s AND challenge_id = %s"
            params = (participation_id, challenge_id)
            participation = common_db.select(conn, query, params)
            print(participation) # Debug
        
        html["name"] = participation[0]["name"]
        html["location"] = participation[0]["location"]
        return html

    # Case B: User opened an empty form for submitting a new participation.
    if not participation_id and not form_data:
        print("Empty form") # Debug
        return html
    
    # Case C: Use has submitted participation data. Validate and insert to database.
    if form_data:
        print("HERE:")
        print(form_data) # Debug
        exit("STOPPED HERE")
        errors = validate_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
            flash(errors)
            html["name"] = form_data["name"]
            html["location"] = form_data["location"]
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
        if not errors:
            # Insert to database and redirect to participation page
            success = insert_participation(challenge_id, form_data)
            if success:
                flash("Osallistumisesi on nyt tallennettu.")
                return redirect(f"/osallistuminen/{challenge_id}/{participation_id}")

            raise Exception("Error in new_participation.py")
            # Todo: handle database errors

    # Case: Something went wrong.
    print("Error")
    print(challenge_id)
    print(participation_id)
    print(form_data)
    raise Exception("Error in new_participation.py")

    """    
    # If user already submitted data, use that to fill in the form.
    if form_data:
        if insert_participation(challenge_id, form_data):
            flash("Osallistumisesi on nyt tallennettu.")
        else:
            flash("Tarkista lomakkeen tiedot ja yritä uudelleen.")

    # If no form_data, show an empty form for a new submission.
    else:
        print("Unknown case") # Debug
        
    print(g.token)
    print(g.user_data)
    """

    