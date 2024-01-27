# Controller for a page which accepts POST data of a participation and inserst or updates it to the database.
# Available for logged in users.


import datetime
import time
from flask import g, flash, redirect
from helpers import common_db
from helpers import common_helpers

def insert_participation(challenge_id, participation_id, form_data):
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
            success = common_db.transaction(conn, query, params)

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
        success = common_db.transaction(conn, query, params)

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
    if not form_data["participant_name"]:
        errors += "Osallistujan nimi puuttuu."
    if not form_data["participation_location"]:
        errors += "Paikka puuttuu."

    # Todo: Check if this is needed
    if not form_data["challenge_id"]:
        errors += "participation_id puuttuu."
    if not form_data["participation_id"]:
        errors += "participation_id puuttuu."

    return errors

"""
def main(form_data):
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
    success = insert_participation(challenge_id, participation_id, form_data)
    print(success)
    if success:
        print("CASE C2 A")
        flash("Osallistumisesi on nyt tallennettu.")
        return redirect(f"/osallistuminen/{challenge_id}/{participation_id}")

    print("CASE C2 B")
    raise Exception("Error in new_participation.py")
    # Todo: handle database errors
"""