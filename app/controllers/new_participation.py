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
            form_data["name"],
            form_data["place"],
            g.user_data["id"],
            now,
            challenge_id,
            participation_id,
        )

        with common_db.connection() as conn:
            query = "UPDATE participations SET name = %s, place = %s, meta_edited_by = %s, meta_edited_at = %s WHERE challenge_id = %s AND participation_id = %s"
            success = common_db.transaction(conn, query, params)

        # Return success and existing participation ID
        return success, participation_id

    # CASE 2: Insert new participation
    # Insert form data into the database
    print("CASE 2")
    params = (
        challenge_id,
        form_data["name"],
        form_data["place"],
        g.user_data["id"],
        now,
        g.user_data["id"],
        now
    )

    with common_db.connection() as conn:
        query = "INSERT INTO participations (challenge_id, name, place, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        success, id = common_db.transaction(conn, query, params)
        print("Success: ", success)

    # Return success and new participation ID returned by the database
    return success, id


def validate_participation_data(form_data):
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
    if not form_data["name"]:
        errors += "osallistujan nimi puuttuu. "
    if not form_data["place"]:
        errors += "paikka puuttuu. "

    if errors:
        errors = "Tarkista lomakkeen tiedot: " + errors
    else:
        errors = False

    return errors



def main(challenge_id_untrusted, participation_id_untrusted, form_data = None):
    html = dict()

    # Get challenge and participation IDs from URL
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

    html["challenge_id"] = challenge_id
    html["participation_id"] = participation_id

    # Todo: Check if this is needed
    if html["participation_id"] == None:
        html["participation_id"] = ""

    # Check that challenge exists and is open
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE challenge_id = %s AND status = 'open'"
        params = (challenge_id,)
        challenge = common_db.select(conn, query, params)

    # CASE X: Challenge cannot be found or participation is closed
    # Todo: Allow user to view, edit and remove their own participation even if the challenge is closed or draft 
    if not challenge:
        print("CASE X")
        flash("Haastetta ei löytynyt tai siihen ei voi enää osallistua.")
        return {"redirect": True, "url": "/"}

    # Get challenge information
    html["challenge_name"] = challenge[0]["title"]

    # Case A: User opened an existing participation for editing.
    # http://localhost:8081/osallistuminen/a04c89f9-bc6f-11ee-837a-0242c0a8a002/1
    if participation_id and not form_data:
        print("CASE A")
        # Load participation data from the database
        with common_db.connection() as conn:
            query = "SELECT * FROM participations WHERE participation_id = %s AND challenge_id = %s"
            params = (participation_id, challenge_id)
            participation = common_db.select(conn, query, params)
            print(participation) # Debug

        # Check that participation exists
        if not participation:
            flash("Osallistumista ei löytynyt.")
            return {"redirect": True, "url": "/"}
        
        # Todo: have form data under single key
        html["data_fields"] = participation[0]

        return html

    # Case B: User opened an empty form for submitting a new participation.
    if not participation_id and not form_data:
        print("CASE B")
        html["data_fields"] = dict()
        return html
    
    # Case C: User has submitted participation data. Validate and insert to database.
    if form_data:
        print("CASE C")
        errors = validate_participation_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
            print("CASE C1")
            flash(errors)

            html["data_fields"] = form_data
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
        print("CASE C2")
        # Insert to database and redirect to participation page
        success, id = save_participation(challenge_id, participation_id, form_data)
        if success:
            flash("Osallistumisesi on nyt tallennettu.")
            return {"redirect": True, "url": f"/osallistuminen/{ challenge_id }/{ id }"}

        raise Exception("Error in saving participation to database.")
        # Todo: handle database errors
    