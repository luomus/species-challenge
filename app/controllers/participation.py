# Controller for a form to submit new participation to a challenge.
# Available for logged in users.

import datetime
from flask import g, flash
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
            g.user_data["id"]
        )

        with common_db.connection() as conn:
            query = "UPDATE participations SET name = %s, place = %s, meta_edited_by = %s, meta_edited_at = %s WHERE challenge_id = %s AND participation_id = %s AND meta_created_by = %s"
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
    Validates and sanitized form data.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        tuple: A tuple containing:
            - error_message (str or False): If validation errors are found, a 
              string with the error message is returned. If no errors are 
              found, False is returned.
            - sanitized_form_data (dict): The form data dictionary with 
              sanitized values.
    """
    errors = ""
    print("form_data: ", form_data)

    # Validate form data
    if not form_data["name"]:
        errors += "osallistujan nimi puuttuu. "
    else:
        if len(form_data["name"]) > 120:
            errors += "osallistujan nimi on liian pitkä, maksimi 120 merkkiä. "
    if not form_data["place"]:
        errors += "paikka puuttuu. "
    else:
        if len(form_data["place"]) > 120:
            errors += "paikka on liian pitkä, maksimi 120 merkkiä. "

    form_data["name"] = common_helpers.sanitize_name(form_data["name"].strip())
    form_data["place"] = common_helpers.sanitize_name(form_data["place"].strip())

    if errors:
        errors = "Tarkista lomakkeen tiedot: " + errors
    else:
        errors = False

    return errors, form_data


def get_challenge(challenge_id):
    """
    Gets challenge data from the database.

    Args:
        challenge_id (int): The challenge ID.

    Returns:
        dict: The challenge data as a dictionary.
    """
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE challenge_id = %s"
        params = (challenge_id,)
        challenge = common_db.select(conn, query, params)

    return challenge[0]


def get_participation(challenge_id, participation_id):
    """
    Gets participation data from the database.

    Args:
        challenge_id (int): The challenge ID.
        participation_id (int): The participation ID.
    
    Returns:
        dict: The participation data as a dictionary.
    """
    params = (participation_id, challenge_id, g.user_data["id"])

    with common_db.connection() as conn:
        query = "SELECT * FROM participations WHERE participation_id = %s AND challenge_id = %s AND meta_created_by = %s"
        participation = common_db.select(conn, query, params)
    
    return participation[0]


def main(challenge_id_untrusted, participation_id_untrusted, form_data = None):
    html = dict()

    # Get challenge and participation IDs from URL
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

    html["challenge_id"] = challenge_id
    html["participation_id"] = participation_id

    print("challenge_id: ", challenge_id)
    print("participation_id: ", participation_id)

    # Jinja template needs these to be empty strings instead of None
    if html["participation_id"] == None:
        html["participation_id"] = ""

    # Get challenge data to see that it exists and if it is draft/open/closed.
    challenge = get_challenge(challenge_id)

    # CASE X: Challenge cannot be found or participation is closed
    # Todo: Allow user to view, edit and remove their own participation even if the challenge is closed or draft 
    if not challenge:
        print("CASE X")
        flash("Haastetta ei löytynyt.")
        return {"redirect": True, "url": "/"}

    html["challenge"] = challenge

    # Case A: User opened an existing participation for editing.
    # http://localhost:8081/osallistuminen/a04c89f9-bc6f-11ee-837a-0242c0a8a002/1
    if participation_id and not form_data:
        print("CASE A")

        # Show warning if challenge is closed or draft, but still allow editing.
        if challenge["status"] != "open":
            flash("Tämä haaste on suljettu. Et voi muokata havaittuja lajeja.")

        # Load participation data from the database with this user.
        participation = get_participation(challenge_id, participation_id)

        # Check that participation exists.
        if not participation:
            flash("Tätä osallistumista ei löytynyt tililtäsi.")
            return {"redirect": True, "url": "/"}
        
        # Todo: have form data under single key
        html["data_fields"] = participation

        return html

    # Case B: User opened an empty form for submitting a new participation.
    if not participation_id and not form_data:
        print("CASE B")

        # Allow adding participation only if challenge is open
        if challenge["status"] != "open":
            flash("Tätä haastetta ei ole olemassa tai siihen ei voi enää osallistua.")
            return {"redirect": True, "url": "/"}

        # Setup empty form
        html["data_fields"] = dict()
        return html
    
    # Case C: User has submitted participation data. Validate and insert to database.
    if form_data:
        print("CASE C")

        # Convert to normal dictionary for sanitization
        form_data = form_data.to_dict()
        errors, form_data = validate_participation_data(form_data)

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
            print("CASE C2 SUCCESS")
            flash("Osallistumisesi on nyt tallennettu.")
            return {"redirect": True, "url": f"/osallistuminen/{ challenge_id }/{ id }"}

        # Database error or trying to edit someone else's participation
        print("CASE C2 FAIL")
        flash("Tietojen tallennus epäonnistui, kokeile uudelleen.")
        return {"redirect": True, "url": "/osallistuminen/{ challenge_id }/{ id }"}
    