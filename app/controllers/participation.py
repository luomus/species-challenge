# Controller for a form to edit and submit participation to a challenge.
# Available for logged in users.

import datetime
from flask import g, flash
from helpers import common_db
from helpers import common_helpers
import json


def make_taxa_html(taxon_id, taxa_dates_json = None):
    """
    Generates a list of species names and date input fields for a given higher taxon.

    Args:
        taxon_id (str): The ID of the higher taxon.
        taxa_dates_json (str, optional): A JSON string containing the species names and dates. Defaults to None.

    Returns:
        str: The HTML code for the list of species names and date input fields.
    """
    html = ""

    taxa_dates = {} # Empty dictionary for new participations
    if taxa_dates_json:
        taxa_dates = json.loads(taxa_dates_json)

    taxa_names = common_helpers.load_taxon_file(taxon_id)

    for key, taxon in taxa_names.items():
        html += f"<li><span>{ taxon['fi'] } (<em>{ taxon['sci'] }</em>)</span> <input type='date' name='taxa:{ key }' value='{ taxa_dates.get(key, '') }'></li>\n"

    html = f"<ul id='taxa'>\n{ html }</ul>\n"
    return html


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
    if participation_id:
        print("CASE 1: UPDATE")
        params = (
            form_data["name"],
            form_data["place"],
            form_data["taxa_count"],
            form_data["taxa_json"],
            g.user_data["id"],
            now,
            form_data["trashed"],
            challenge_id,
            participation_id,
            g.user_data["id"] # Only allow editing if user is the creator
        )

        with common_db.connection() as conn:
            query = "UPDATE participations SET name = %s, place = %s, taxa_count = %s, taxa_json = %s, meta_edited_by = %s, meta_edited_at = %s, trashed = %s WHERE challenge_id = %s AND participation_id = %s AND meta_created_by = %s"
            success, _ = common_db.transaction(conn, query, params)

        # Return success and existing participation ID
        return success, participation_id

    # CASE 2: Insert new participation
    # Insert form data into the database
    print("CASE 2: INSERT")
    params = (
        challenge_id,
        form_data["name"],
        form_data["place"],
        form_data["taxa_count"],
        form_data["taxa_json"],
        form_data["trashed"],
        g.user_data["id"],
        now,
        g.user_data["id"],
        now
    )

    with common_db.connection() as conn:
        query = "INSERT INTO participations (challenge_id, name, place, taxa_count, taxa_json, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        success, id = common_db.transaction(conn, query, params)

    return success, id


def taxa_to_dict(form_data):
    taxa_data = {}
    prefix = "taxa:"

    for key, value in form_data.items():
        if key.startswith(prefix):
            _, qname = key.split(':')
            taxa_data[qname] = value

    return taxa_data


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

    # Name
    if not form_data["name"]:
        errors += "osallistujan nimi puuttuu. "
    else:
        if len(form_data["name"]) > 120:
            errors += "osallistujan nimi on liian pitkä, maksimi 120 merkkiä. "

    # Place
    if not form_data["place"]:
        errors += "paikka puuttuu. "
    else:
        if len(form_data["place"]) > 120:
            errors += "paikka on liian pitkä, maksimi 120 merkkiä. "

    # Sanitize field values
    form_data["name"] = common_helpers.sanitize_name(form_data["name"].strip())
    form_data["place"] = common_helpers.sanitize_name(form_data["place"].strip())

    # Handle taxon data
    # 1) Extract taxon data from form data
    taxa_data = taxa_to_dict(form_data)

    # 2) Remove empty values
    taxa_data = {k: v for k, v in taxa_data.items() if v}
    
    # 3) Remove values that are not YYYY-MM-DD dates
    for key, value in taxa_data.items():
        if not common_helpers.is_yyyy_mm_dd(value):
            del taxa_data[key]

    # 4) Calculate number of species
    form_data["taxa_count"] = len(taxa_data)

    # 5) Convert to JSON string (for database JSON field) where dates are YYYY-MM-DD
    # Note: form_data still has the original taxon data
    form_data["taxa_json"] = json.dumps(taxa_data)

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

    # If participation not found with these parameters, return False
    if not participation:
        return False
    
    return participation[0]


def main(challenge_id_untrusted, participation_id_untrusted, form_data = None):

    # Default values
    html = dict()
    html["public_selected"] = "selected='selected'"
    html["trashed_selected"] = ""

    # Get challenge and participation IDs from URL
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

    html["challenge_id"] = challenge_id
    html["participation_id"] = participation_id

    # Jinja template needs these to be empty strings instead of None
    if html["participation_id"] == None:
        html["participation_id"] = ""

    # Get challenge data to see that it exists and if it is draft/open/closed.
    challenge = get_challenge(challenge_id)

    # CASE X: Challenge cannot be found or participation is closed
    if not challenge:
        print("CASE X")
        flash("Haastetta ei löytynyt.", "info")
        return {"redirect": True, "url": "/"}

    html["challenge"] = challenge

    # Case A: User opened an empty form for submitting a new participation.
    if not participation_id and not form_data:
        print("CASE A")

        # Allow adding participation only if challenge is open
        if challenge["status"] != "open":
            flash("Tätä haastetta ei ole olemassa tai siihen ei voi enää osallistua.", "info")
            return {"redirect": True, "url": "/"}

        # Setup empty form
        html['taxa'] = make_taxa_html(challenge["taxon"])
        html["data_fields"] = dict()
        return html
    
    # Case B: User opened an existing participation for editing.
    # Example: http://localhost:8081/osallistuminen/4/6
    if participation_id and not form_data:
        print("CASE B")

        # Show warning if challenge is closed or draft, but still allow editing.
        if challenge["status"] != "open":
            flash("Tämä haaste on suljettu. Et voi muokata havaittuja lajeja.", "info")

        # Load participation data from the database with this user.
        participation = get_participation(challenge_id, participation_id)

        # Check that participation exists.
        if not participation:
            flash("Tätä osallistumista ei löytynyt tililtäsi.", "info")
            return {"redirect": True, "url": "/"}
        
        html['taxa'] = make_taxa_html(challenge["taxon"], participation["taxa_json"])
        html["data_fields"] = participation

        # Change default trashed value based on database value
        if participation["trashed"]:
            html["trashed_selected"] = "selected='selected'"
            html["public_selected"] = ""

        return html

    # Case C: User has submitted participation data. Validate and insert to database.
    if form_data:
        print("CASE C")

        # Convert to normal dictionary for sanitization
        form_data = form_data.to_dict()

        print(form_data) # Debug

        errors, form_data = validate_participation_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
            print("CASE C1")
            flash(errors, "error")

            html["data_fields"] = form_data
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
        print("CASE C2")
        success, id = save_participation(challenge_id, participation_id, form_data)

        if success:
            print("CASE C2 SUCCESS")
            flash("Osallistumisesi on nyt tallennettu.", "success")
            return {"redirect": True, "url": f"/osallistuminen/{ challenge_id }/{ id }"}

        # Database error or trying to edit someone else's participation
        print("CASE C2 FAIL")
        raise Exception("Error saving participation to database.")
    