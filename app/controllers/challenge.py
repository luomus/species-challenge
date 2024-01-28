# Controller for a form to edit and submit a challenge.
# Available for admin users.

import datetime
from flask import g, flash
from helpers import common_db
from helpers import common_helpers


def save_challenge(challenge_id, form_data):
    """
    Inserts challenge data to the database.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        bool: True if the form data was successfully validated and inserted, False otherwise.
    """

    # Current datetime in MySQL format
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # CASE 1: Edit existing challenge
    # Update form data in the database
    if challenge_id:
        print("CASE 1")
        params = (
            form_data["taxon"],
            form_data["year"],
            form_data["type"],
            form_data["title"],
            form_data["status"],
            g.user_data["id"],
            now,
            challenge_id,
        )

        with common_db.connection() as conn:
            query = "UPDATE challenges SET taxon = %s, year = %s, type = %s, title = %s, status = %s, meta_edited_by = %s, meta_edited_at = %s WHERE challenge_id = %s"
            success = common_db.transaction(conn, query, params)

        # Return success and existing challenge ID
        return success, challenge_id

    # CASE 2: Insert new challenge
    # Insert form data into the database
    print("CASE 2")
    print(form_data)
    params = (
        form_data["taxon"],
        form_data["year"],
        form_data["type"],
        form_data["title"],
        form_data["status"],
        g.user_data["id"],
        now,
        g.user_data["id"],
        now
    )

    print("PARAMS:", params)

    with common_db.connection() as conn:
        query = "INSERT INTO challenges (taxon, year, type, title, status, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        success, id = common_db.transaction(conn, query, params)

    print("DEBUG: ", success, id) # Debug

    # Return success and new challenge ID returned by the database
    return success, id


def validate_challenge_data(form_data):
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

    # Validate form data
    if not form_data["title"]:
        errors += "haasteen nimi puuttuu. "
    else:
        if len(form_data["title"]) > 240:
            errors += "haasteen nimi on liian pitkä, maksimi 240 merkkiä. "
    if not form_data["taxon"]:
        errors += "taksoni puuttuu. "
    else:
        if len(form_data["taxon"]) > 16:
            errors += "taksoni on liian pitkä, maksimi 16 merkkiä. "
    if not form_data["year"]:
        errors += "vuosi puuttuu. "
    # Check that year is a number
    if not common_helpers.is_year(form_data["year"]):
        errors += "vuoden pitää olla numero. "

    # Todo: more validations

    # Sanitize field values
    form_data["title"] = common_helpers.sanitize_name(form_data["title"].strip())

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

    if not challenge:
        return False
    return challenge[0]


def main(challenge_id_untrusted = None, form_data = None):
    html = dict()

    # Get challenge and participation IDs from URL
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)

    # Jinja template needs these to be empty strings instead of None
    html["challenge_id"] = challenge_id
    if html["challenge_id"] == None:
        html["challenge_id"] = ""

    # CASE 0: Adding a new challenge with an empty form.
    if not challenge_id and not form_data:
        # Setup empty form
        html["data_fields"] = dict()
        html["challenge"] = dict()

        # Todo: think through how title should be handled
        html["challenge"]["title"] = "(uusi)"
        return html

    # Get challenge data to see that it exists and if it is draft/open/closed.
    challenge = get_challenge(challenge_id)

    # CASE A: Challenge id given, but it does not exist in the database.
    if not challenge and not form_data:
        print("CASE A")
        flash("Haastetta ei löytynyt.")
        return {"redirect": True, "url": "/admin"}

    # Case B: Editing an existing challenge, with a form filled in from the database.
    # Challenge found from the database
    # Example: http://localhost:8081/osallistuminen/4
    if challenge and not form_data:
        print("CASE B")
        html["data_fields"] = challenge
        html["challenge"] = dict()
        html["challenge"]["title"] = challenge["title"]

        return html
    
    # Case C: User has submitted challenge data. Validate and insert to database.
    if form_data:
        print("CASE C")

        # Convert to normal dictionary for sanitization
        form_data = form_data.to_dict()
        print(form_data) # Debug

        errors, form_data = validate_challenge_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
            print("CASE C1")
            flash(errors)
            html["challenge"] = dict()
            html["challenge"]["title"] = form_data["title"]
            html["data_fields"] = form_data
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
        print("CASE C2")
        # Insert to database and redirect to participation page
        success, id = save_challenge(challenge_id, form_data)
        if success:
            print("CASE C2 SUCCESS")
            flash("Haaste on nyt tallennettu.")
            return {"redirect": True, "url": f"/haaste/{ id }"}

        # Database error or trying to edit someone else's participation
        print("CASE C2 FAIL")
        flash("Tietojen tallennus epäonnistui, kokeile uudelleen.")
        return {"redirect": True, "url": f"/haaste/{ challenge_id }/{ id }"}
    