# Controller for a form to edit and submit a challenge.
# Available for admin users.

from flask import g, flash
from helpers import common_db
from helpers import common_helpers
import json
import datetime

def save_challenge(challenge_id, form_data):
    """
    Inserts challenge data to the database.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        bool: True if the form data was successfully validated and inserted, False otherwise.
    """

    print("FORM DATA", form_data)

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
            form_data["description"],
            g.user_data["id"],
            now,
            challenge_id,
        )

        with common_db.connection() as conn:
            query = "UPDATE challenges SET taxon = %s, year = %s, type = %s, title = %s, status = %s, description = %s, meta_edited_by = %s, meta_edited_at = %s WHERE challenge_id = %s"
            success, _ = common_db.transaction(conn, query, params)

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
        form_data["description"],
        g.user_data["id"],
        now,
        g.user_data["id"],
        now
    )

    print("PARAMS CASE 2:", params)

    with common_db.connection() as conn:
        query = "INSERT INTO challenges (taxon, year, type, title, status, description, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        success, id = common_db.transaction(conn, query, params)

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

    # Title
    if not form_data["title"]:
        errors += "Haasteen nimi puuttuu. "
    else:
        if len(form_data["title"]) > 240:
            errors += "Haasteen nimi on liian pitkä, maksimi 240 merkkiä. "

    # Description
    if len(form_data["description"]) > 2000:
        errors += "Haasteen nimi on liian pitkä, maksimi 2000 merkkiä. "

    # Taxon
    if not form_data["taxon"]:
        errors += "Taksoni puuttuu. "
    else:
        # Check if file exists in ./data/{taxon}_taxa.json
        if not common_helpers.taxon_file_exists(form_data["taxon"]):
            errors += f"Taksonin { form_data['taxon'] } lajiluetteloa ei löytynyt: valitse toinen taksoni tai pyydä ylläpitäjää lisäämään luettelo. "

    # Year
    if not form_data["year"]:
        errors += "Vuosi puuttuu. "
    # Check that year is a number
    if not common_helpers.is_year(form_data["year"]):
        errors += "Vuoden pitää olla numero. "

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
    
    # Set all None values to empty strings
    for key, value in challenge[0].items():
        if value == None:
            challenge[0][key] = ""

#    print(challenge[0]) # Debug

    return challenge[0]


def make_option_field_html(field_name, challenge_data = None):
    # Load schema from a CSV file
    filename = "./data/challenge_vocabulary.json"
    with open(filename, "r") as f:
        schema = json.load(f)

    html = ""

    # Selected field
    selected_option = ""
    if challenge_data:
        selected_option = challenge_data[field_name]

    # Generate HTML for option fields
    field = schema["controlledVocabularyFields"][field_name]

    html += f"<label for='{field_name}'>{field['label']['fi']}:</label><br>\n"
    html += f"<select name='{field_name}' id='{field_name}' required>\n"
    html += "    <option value=''>(valitse)</option>\n"
    for option in field["options"]:
        selected = ""
        if option["key"] == selected_option:
            selected = " selected='selected'"
        html += f"    <option value='{option['key']}'{selected}>{option['label']['fi']}</option>\n"
    html += "</select>\n"

    return html


def main(challenge_id_untrusted = None, form_data = None):
    html = dict()

    # Get challenge IDs from URL
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)

    # Jinja template needs these to be empty strings instead of None
    html["challenge_id"] = challenge_id
    if html["challenge_id"] == None:
        html["challenge_id"] = ""


    # CASE A: Adding a new challenge with an empty form.
    if not challenge_id and not form_data:
        print("CASE A")
        # Setup empty form
        html["status_field_html"] = make_option_field_html("status")
        html["type_field_html"] = make_option_field_html("type")
        html["data_fields"] = dict()
        return html

    # Get challenge data to see that it exists and if it is draft/open/closed.
    challenge = get_challenge(challenge_id)

    # CASE B: Challenge id given, but it does not exist in the database.
    if not challenge and not form_data:
        print("CASE B")
        flash("Haastetta ei löytynyt.", "info")
        return {"redirect": True, "url": "/admin"}

    # Case C: Editing an existing challenge, with a form filled in from the database.
    # Challenge found from the database
    # Example: http://localhost:8081/osallistuminen/4
    if challenge and not form_data:
        print("CASE C")

        # Setup form with data
        html["status_field_html"] = make_option_field_html("status", challenge)
        html["type_field_html"] = make_option_field_html("type", challenge)
        html["data_fields"] = challenge

        return html
    
    # Case D: User has submitted challenge data. Validate and insert to database.
    if form_data:
        print("CASE D")

        # Convert to normal dictionary for sanitization
        form_data = form_data.to_dict()

        errors, form_data = validate_challenge_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
            print("CASE C1")
            flash(errors, "error")
            html["data_fields"] = form_data
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
        print("CASE C2")
        success, id = save_challenge(challenge_id, form_data)

        if success:
            print("CASE C2 SUCCESS")
            flash("Haaste on nyt tallennettu.", "success")
            return {"redirect": True, "url": f"/admin/haaste/{ id }"}

        # Database error
        print("CASE C2 FAIL")
        raise Exception("Error saving challenge to database.")
    