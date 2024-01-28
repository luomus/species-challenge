# Controller for a form to submit new participation to a challenge.
# Available for logged in users.

import datetime
import time
from flask import g, flash, redirect, url_for
from helpers import common_db
from helpers import common_helpers

def save_participation(challenge_id, participation_id, form_data):
    """
    Inserts participation data to the database.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        bool: True if the form data was successfully validated and inserted, False otherwise.
    """

    # Current datetime in MySQL format
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # CASE 1: Edit existing participation
    # Update form data in the database
    print("CASE 1")
    if participation_id:
        params = (
            form_data["participant_name"],
            form_data["participation_location"],
            g.user_data["id"],
            now,
            challenge_id,
            participation_id,
        )

        with common_db.connection() as conn:
            query = "UPDATE participations SET participant_name = %s, location = %s, meta_edited_by = %s, meta_edited_at = %s WHERE challenge_id = %s AND id = %s"
            success, id = common_db.transaction(conn, query, params)

        return success

    # CASE 2: Insert new participation
    # Insert form data into the database
    print("CASE 2")
    params = (
        challenge_id,
        form_data["participant_name"],
        form_data["participation_location"],
        g.user_data["id"],
        now,
        g.user_data["id"],
        now
    )

    with common_db.connection() as conn:
        query = "INSERT INTO participations (challenge_id, participant_name, location, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        success, id = common_db.transaction(conn, query, params)
        print("Success: ", success)

    return success, id


def validate_data(form_data):
    """
    Validates the form data.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        string: A validation error message if errors were found.
        False: If no errors were found.
    """
    errors = ""

    # Validate form data
    if not form_data["participant_name"]:
        errors += "osallistujan nimi puuttuu. "
    if not form_data["participation_location"]:
        errors += "paikka puuttuu. "

    if errors:
        errors = "Tarkista lomakkeen tiedot: " + errors
    else:
        errors = False

    return errors



def main(challenge_id_untrusted, participation_id_untrusted, form_data = None):
    html = dict()

    print("Form data:")
    print(form_data) # Debug

    challenge_id = common_helpers.clean_uuid(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

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
        return {"redirect": True, "url": "/"}

    # Get challenge information
    print(challenge) # Debug
    html["challenge_name"] = challenge[0]["name"]

    # Case A: User opened an existing participation for editing.
    # http://localhost:8081/osallistuminen/a04c89f9-bc6f-11ee-837a-0242c0a8a002/1
    if participation_id and not form_data:
        print("CASE A")
        print("part: ", participation_id)
        print("chall: ", challenge_id)
        # Load participation data from the database
        with common_db.connection() as conn:
            query = "SELECT * FROM participations WHERE id = %s AND challenge_id = %s"
            params = (participation_id, challenge_id)
            participation = common_db.select(conn, query, params)
            print(participation) # Debug

        # Check that participation exists
        if not participation:
            print("CASE A1")
            flash("Osallistumista ei löytynyt.")
            return {"redirect": True, "url": "/"}
        
        print("CASE A2")
        html["participant_name"] = participation[0]["participant_name"]
        html["participation_location"] = participation[0]["location"]
        return html

    # Case B: User opened an empty form for submitting a new participation.
    if not participation_id and not form_data:
        print("CASE B")
        print("part: ", participation_id)
        print("chall: ", challenge_id)
        return html
    
    # Case C: User has submitted participation data. Validate and insert to database.
    if form_data:
        print("CASE C")
        print("part: ", participation_id)
        print("chall: ", challenge_id)
        print(form_data) # Debug
        errors = validate_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
            print("CASE C1")
            flash(errors)
            html["participant_name"] = form_data["participant_name"]
            html["participation_location"] = form_data["participation_location"]
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
        print("CASE C2")
        # Insert to database and redirect to participation page
        success, id = save_participation(challenge_id, participation_id, form_data)
        print(success, id) # Debug
        if success:
            print("CASE C2 A")
            flash("Osallistumisesi on nyt tallennettu.")
            return {"redirect": True, "url": f"/osallistuminen/{ challenge_id }/{ id }"}

        print("CASE C2 B")
        raise Exception("Error in new_participation.py")
        # Todo: handle database errors


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

    