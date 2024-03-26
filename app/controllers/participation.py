# Controller for a form to edit and submit participation to a challenge.
# Available for logged in users.

import datetime
from flask import g, flash
from helpers import common_db
from helpers import common_helpers
import json
import os


def make_taxa_html(challenge, taxa_dates_json = None):
    """
    Generates a list of species names and date input fields for a given higher taxon.

    Args:
        taxon_id (str): The ID of the higher taxon.
        taxa_dates_json (str, optional): A JSON string containing the species names and dates. Defaults to None.

    Returns:
        str: The HTML code for the list of species names and date input fields.
    """

    taxon_file_id = challenge["taxon"]

    # Min and max dates for date input fields
    min_date = f"{ challenge['year'] }-01-01"
    max_date = f"{ challenge['year'] }-12-31"
    # However, if max_date is in the future, make it today instead
    if max_date > datetime.datetime.now().strftime("%Y-%m-%d"):
        max_date = datetime.datetime.now().strftime("%Y-%m-%d")

    basic_taxa_html = ""
    additional_taxa_html = ""

    # Taxa names and dates form the participation (from database)
    # Default empty dictionary for new participations
    taxa_dates = {}
    if taxa_dates_json:
        taxa_dates = json.loads(taxa_dates_json)
    """
    taxa_dates sample: 
    {'MX.37691': '2024-01-11', 'MX.37721': '2024-01-02', 'MX.37717': '2024-01-27', 'MX.37719': '2024-01-28', 'MX.37763': '2024-01-10', 'MX.37771': '2024-01-18', 'MX.4994055': '2024-01-18', 'MX.37752': '2024-01-30', 'MX.40138': '2024-01-30', 'MX.40150': '2024-01-30', 'MX.39201': '2024-01-30', 'MX.4973227': '2024-01-17', 'MX.39827': '2024-01-25', 'MX.39917': '2024-01-30'}

    """

    # Basic taxa names of this challenge
    taxa_names = common_helpers.load_taxon_file(taxon_file_id)
    """
    taxa_names sample:
    {
        "MX.43922": {
        "sci": "Pohlia nutans",
        "fi": "nuokkuvarstasammal",
        "swe": "vanlig nickmossa"
        },
        "MX.43502": {
        "sci": "Climacium dendroides",
        "fi": "palmusammal",
        "swe": "palmmossa"
        }
    }
    """

    # All taxa names of the higher taxon (e.g. plants)
    all_taxa_names = common_helpers.load_taxon_file(taxon_file_id + "_all")

#    print("ALL TAXA NAMES: ", all_taxa_names)
    # Todo: refactoring

    # Loop taxa_names, i.e. the basic taxa
    for taxon_id, taxon_data in taxa_names.items():

        # Subheadings defined in taxon file 
        if "heading" in taxon_data:
            basic_taxa_html += f"<li class='list_heading_4'><h4>{ taxon_data['heading'] }</h4></li>\n"

        # Add to basic_taxa_html, fill in with date from taxa_dates if found
        id_html = taxon_id.replace(".", "_").replace(" ", "")
        fin_html = taxon_data.get("fin", "")
        swe_html = taxon_data.get("swe", "")
        if swe_html:
            swe_html = f", { swe_html }"
        sci_html = taxon_data.get("sci", "")
        basic_taxa_html += f"""
            <li>
                <span class='taxon_name' id='{ id_html }_id' title='Merkitse havaintopäivä tälle lajille'>{ fin_html.capitalize() }{ swe_html } (<em>{ sci_html }</em>)</span>
                <input title='Valitse havaintopäivä tälle lajille' type='date' id={ id_html } name='taxa:{ taxon_id }' value='{ taxa_dates.get(taxon_id, '') }' min='{ min_date }' max='{ max_date }'>
                <span class='clear_date' id='clear-{ id_html }' title='Poista havaintopäivä'>❌</span>
                <a href='https://laji.fi/taxon/{ taxon_id }' target='_blank' class='taxon_info' title='Lisätietoa tästä lajista'>i</a>
            </li>\n"""

        # Remove taxon_id from taxa_dates, so that it won't be added to additional_taxa_html
        if taxon_id in taxa_dates:
            del taxa_dates[taxon_id]

    # Loop remaining taxa_dates, i.e. the additional taxa
    for observed_taxon_id, observed_taxon_date in taxa_dates.items():

        # Add to additional_taxa_html
        # Check if taxon exists in all_taxa_names. Might not if it has been added to Laji.fi after the taxon list on this app has been set up.
        fin = "" # default
        swe = "" # default
        sci = observed_taxon_id # default
        if observed_taxon_id in all_taxa_names:
            sci = all_taxa_names[observed_taxon_id]["sci"]
            # Finnish name might not exist
            if "fin" in all_taxa_names[observed_taxon_id]:
                fin = all_taxa_names[observed_taxon_id]["fin"]
    
            # Swedish name might not exist
            if "swe" in all_taxa_names[observed_taxon_id]:
                swe = all_taxa_names[observed_taxon_id]["swe"]

            if swe:
                swe = f", { swe }"
    
        additional_taxa_html += f"""
            <li>
                <span class='taxon_name'>{ fin.capitalize() }{ swe } (<em>{ sci }</em>)</span>
                <input type='date' id='{ id_html }_id_additional' name='taxa:{ observed_taxon_id }' value='{ observed_taxon_date }' min='{ min_date }' max='{ max_date }'>
                <a href='https://laji.fi/taxon/{ observed_taxon_id }' target='_blank' class='taxon_info' title='Lisätietoa tästä lajista'>i</a>
            </li>\n"""

    # Combine into a list
    html = f"""
        <ul id='taxa'>\n
        <li class='list_heading_3'><h3>Peruslistan ulkopuoliset lajit:</h3></li>\n
            { additional_taxa_html }
        <li class='list_heading_3'><h3>Peruslistan lajit:</h3></li>\n
            { basic_taxa_html }
        </ul>\n
        """

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
#        print("CASE 1: UPDATE")
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
#    print("CASE 2: INSERT")
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
        query = "INSERT INTO participations (challenge_id, name, place, taxa_count, taxa_json, trashed, meta_created_by, meta_created_at, meta_edited_by, meta_edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
    if not "name" in form_data:
        errors += "osallistujan nimi puuttuu. "
    else:
        form_data["name"] = common_helpers.sanitize_name(form_data["name"].strip())
        if len(form_data["name"]) > 120:
            errors += "osallistujan nimi on liian pitkä, enintään 120 merkkiä. "

    # Place
    if "place" in form_data:
        form_data["place"] = common_helpers.sanitize_name(form_data["place"].strip())
        if len(form_data["place"]) > 120:
            errors += "paikannimi on liian pitkä, enintään 120 merkkiä. "
    else:
        form_data["place"] = ""

    # Handle taxon data
    # 1) Extract taxon data from form data
    taxa_data = taxa_to_dict(form_data)

    # 2) Remove empty values
    # Todo: is this needed anymore?
    taxa_data = {k: v for k, v in taxa_data.items() if v}
    
    # 3) Remove values that are not YYYY-MM-DD dates
    for key, value in taxa_data.items():
        if not common_helpers.is_yyyy_mm_dd(value):
            del taxa_data[key]

    # 4) Add trashed if not present
    if "trashed" not in form_data:
        form_data["trashed"] = False

    # 5) Calculate number of species
    form_data["taxa_count"] = len(taxa_data)

    # 6) Convert to JSON string (for database JSON field) where dates are YYYY-MM-DD
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


def main(challenge_id_untrusted, participation_id_untrusted, form_data = None):

    # Default values
    html = dict()
    html["finbif_access_token"] = os.environ.get("FINBIF_API_TOKEN")
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
#        print("CASE X")
        flash("Haastetta ei löytynyt.", "info")
        return {"redirect": True, "url": "/"}

    html["challenge"] = challenge

    # Todo: min and max dates from database

    # Case A: User opened an empty form for submitting a new participation.
    if not participation_id and not form_data:
#        print("CASE A")

        # Allow adding participation only if challenge is open
        if challenge["status"] != "open":
            flash("Tätä haastetta ei ole olemassa tai siihen ei voi enää osallistua.", "info")
            return {"redirect": True, "url": "/"}

        # Setup empty form
        html['taxa'] = make_taxa_html(challenge)
        html["data_fields"] = dict()
        return html
    
    # Case B: User opened an existing participation for editing.
    # Example: http://localhost:8081/osallistuminen/4/6
    if participation_id and not form_data:
#        print("CASE B")

        # Show warning if challenge is closed or draft, but still allow editing.
        if challenge["status"] != "open":
            flash("Tämä haaste on suljettu. Et voi muokata havaittuja lajeja.", "info")

        # Load participation data from the database with this user.
        participation = common_helpers.get_participation(challenge_id, participation_id)
        html['participation'] = participation

        # Check that participation exists.
        if not participation:
            flash("Tätä osallistumista ei löytynyt tililtäsi.", "info")
            return {"redirect": True, "url": "/"}
        
        html['taxa'] = make_taxa_html(challenge, participation["taxa_json"])
        html["data_fields"] = participation

        # Change default trashed value based on database value
        if participation["trashed"]:
            html["trashed_selected"] = "selected='selected'"
            html["public_selected"] = ""

        return html

    # Case C: User has submitted participation data. Validate and insert to database.
    if form_data:
#        print("CASE C")

        # Convert to dict removing empty fields.
        # Empty taxon fields need to be removed so that if user adds a basic taxon using additional taxa ui, it won't be removed when the raw data is converted to dict using to_dict(), which allows only one value per key (i.e. throws away the value from additional taxa ui).
        # Note that optional empty fields like "place" need to be put back to the form data - this is donw at validation step.
        # Todo: Maybe instead remove only empty taxon fields here?
        form_data = {key: value for key, value in form_data.items(multi=True) if value}

        errors, form_data = validate_participation_data(form_data)

        # Case C1: Errors found. Show the form again with error messages.
        if errors:
#            print("CASE C1")
            flash(errors, "error")

            html["data_fields"] = form_data
            return html
        
        # Case C2: No errors found. Insert to database and redirect to participation page.
#        print("CASE C2")
        success, id = save_participation(challenge_id, participation_id, form_data)
        if success:
#            print("CASE C2 SUCCESS")
            flash("Osallistumisesi on nyt tallennettu.", "success")
            return {"redirect": True, "url": f"/osallistuminen/{ challenge_id }/{ id }"}

        # Database error or trying to edit someone else's participation
#        print("CASE C2 FAIL")
        raise Exception("Error saving participation to database.")
