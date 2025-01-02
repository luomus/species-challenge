# Common helpers functions.

import requests
import json
import sys
import os
import re
from flask import g

from helpers import common_db

def fetch_finbif_api(api_url, log = False):
    """
    Fetches data from the FINBIF API.

    Args:
    api_url (str): The API URL to fetch data from.
    log (bool): Optional; If True, logs the URL to stdout. Defaults to False.

    Returns:
    dict: A dictionary containing the API response data.

    Raises:
    ConnectionError: If there is an issue connecting to the API.
    """
#    if "access_token=" not in api_url:
#        print("WARNING: access_token param is missing from your url!", file = sys.stdout)

    api_url = api_url + os.environ.get('FINBIF_API_TOKEN')
#    print("Fetching API: " + api_url, file = sys.stdout)

    if log:
        print(api_url, file = sys.stdout)

    try:
        r = requests.get(api_url)
    except ConnectionError:
        print("ERROR: api.laji.fi error.", file = sys.stdout)

    data_json = r.text
    data_dict = json.loads(data_json)

    if "status" in data_dict:
        if 403 == data_dict["status"]:
            print("ERROR: api.laji.fi 403 error.", file = sys.stdout)
            raise ConnectionError

    return data_dict


def fetch_lajiauth_api(api_url, log = False):
    """
    Fetches data from the FINBIF Laji-Auth API.

    Args:
    api_url (str): The API URL to fetch data from.
    log (bool): Optional; If True, logs the URL to stdout. Defaults to False.

    Returns:
    dict: A dictionary containing the API response data.

    Raises:
    ConnectionError: If there is an issue connecting to the API.
    """
#    print("Fetching API: " + api_url, file = sys.stdout)

    if log:
        print(api_url, file = sys.stdout)

    try:
        r = requests.get(api_url)
    except ConnectionError:
        print("ERROR: laji-auth api error.", file = sys.stdout)

    data_json = r.text
    data_dict = json.loads(data_json)

    if "status" in data_dict:
        if 403 == data_dict["status"]:
            print("ERROR: laji-auth api 403 error.", file = sys.stdout)
            raise ConnectionError

    return data_dict


def clean_token(input_string):
    """
    Validates if a given string contains only alphanumeric characters.

    Args:
    input_string (str): The string to validate.

    Returns:
    str: The input_string if it is alphanumeric.

    Raises:
    ValueError: If the input_string contains disallowed characters.
    """
    for character in input_string:
        if not character.isalnum():
            raise ValueError("Token contains disallowed characters.")

    return input_string


def clean_int(input_string):
    """
    Validates if a given string is a valid integer

    Args:
    input_string (str): The string to validate.

    Returns:
    int: The input_string converted to integer.
    None: if the input_string is None.

    Raises:
    ValueError: If the input_string cannot be converted to integer.
    """
    if not input_string:
        return None
    try:
        return int(input_string)
    except ValueError:
        raise ValueError("Input is not an integer.")
    

def sanitize_name(name):
    # Allow Unicode letter characters, spaces, hyphens, and apostrophes
    pattern = re.compile(r'[^\w\s\'-]', re.UNICODE)
    return pattern.sub('', name)


def is_yyyy_mm_dd(input_string):
    """
    Validates if a given string is a valid date in YYYY-MM-DD format.

    Args:
    input_string (str): The string to validate.

    Returns:
    bool: True if the input_string is a valid date in YYYY-MM-DD format,
    False otherwise.
    """
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(pattern.match(input_string))


def valid_taxon_qname(input_string):
    """
    Validates if a given string is a valid taxon QName.

    Args:
    input_string (str): The string to validate.

    Returns:
    bool: True if the input_string is a valid taxon QName,
    False otherwise.
    """
    pattern = r'^MX\.\d+$'
    return bool(re.match(pattern, input_string))


def taxon_file_exists(taxon_file_id):
    """
    Checks if all necessary taxon files exist in data and static directories.

    Args:
    taxon_file_id (str): The taxon file id (from database).

    Returns:
    bool: True if all the files exists, False otherwise.
    """

    # Loop filenames to check if all of them exist
    files_to_check = []
    files_to_check.append("./data/" + taxon_file_id + ".json")
    files_to_check.append("./data/" + taxon_file_id + "_all.json")
    files_to_check.append("./static/taxa/" + taxon_file_id + "_all.json")

    for filename in files_to_check:
        if not os.path.isfile(filename):
            return False

    return True


def load_taxon_file(taxon_file_id):
    """
    Loads a taxon file from ./data/{taxon_file_id}.json.

    Args:
    taxon_id (str): The taxon file id (from database).

    Returns:
    dict: A dictionary containing the taxon file data.
    """
    file_path = f"./data/{ taxon_file_id }.json"
    print(file_path)

    with open(file_path, 'r') as file:
        taxa_names = json.load(file)

    return taxa_names



def get_challenge(challenge_id):
    params = (challenge_id,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE challenge_id = %s"
        data = common_db.select(conn, query, params)

    if data:
        return data[0]
    return {}


def get_all_participations(challenge_id):
    with common_db.connection() as conn:
        query = "SELECT * FROM participations WHERE challenge_id = %s and trashed = 0 ORDER BY taxa_count DESC"
        params = (challenge_id,)
        participations = common_db.select(conn, query, params)

    return participations


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


def make_taxa_html(participations, challenge_data, taxa_json = ""):
    taxon_id = challenge_data["taxon"]
    print(challenge_data)
    '''
    participations -variable contains data like this:
    [
        {
            'participation_id': 5, 
            'challenge_id': 4, 
            'name': 
            'Nimi Merkkinen', 'place': 
            'Nimismiehenkylä', 'taxa_count': 28, 
            'taxa_json': '{"MX.37691": "2024-01-30", "MX.37721": "2024-01-30", "MX.37717": "2024-01-17", "MX.37719": "2024-01-25", "MX.37763": "2024-01-01", "MX.37771": "2024-01-30", "MX.4994055": "2024-01-03", "MX.37752": "2024-01-30", "MX.37747": "2024-01-30", "MX.37826": "2024-01-30", "MX.37812": "2024-01-10", "MX.37819": "2024-01-30", "MX.40138": "2024-01-30", "MX.39201": "2024-01-30", "MX.39235": "2024-01-30", "MX.4973227": "2024-01-17", "MX.39887": "2024-01-30", "MX.39917": "2024-01-11", "MX.38279": "2024-01-02", "MX.38598": "2024-01-13", "MX.39052": "2024-01-20", "MX.39038": "2024-01-11", "MX.39465": "2024-01-18", "MX.39673": "2024-01-30", "MX.39967": "2024-01-30", "MX.38301": "2024-01-30", "MX.40632": "2024-01-11", "MX.38843": "2024-01-25"}', 
            'meta_created_by': 'MA.3', 
            'meta_created_at': datetime.datetime(2024, 1, 28, 15, 19, 17), 
            'meta_edited_by': 'MA.3', 
            'meta_edited_at': datetime.datetime(2024, 1, 31, 11, 37, 2), 
            'trashed': 0
        },
        {
            'participation_id': 6, 
            'challenge_id': 4, 
            'name': "André D'Artágnan", 
            'place': 'Ääkkölä ääkkölärules', 
            'taxa_count': 14, 
            'taxa_json': '{"MX.37691": "2024-01-11", "MX.37721": "2024-01-02", "MX.37717": "2024-01-27", "MX.37719": "2024-01-28", "MX.37763": "2024-01-10", "MX.37771": "2024-01-18", "MX.4994055": "2024-01-18", "MX.37752": "2024-01-30", "MX.40138": "2024-01-30", "MX.40150": "2024-01-30", "MX.39201": "2024-01-30", "MX.4973227": "2024-01-17", "MX.39827": "2024-01-25", "MX.39917": "2024-01-30"}', 
            'meta_created_by': 'MA.3', 
            'meta_created_at': datetime.datetime(2024, 1, 28, 15, 29, 1), 
            'meta_edited_by': 'MA.3', 
            'meta_edited_at': datetime.datetime(2024, 1, 31, 11, 34, 47), 
            'trashed': 0
        }
    ]
    '''
    if not participations:
        return "<p>Yhtään lajia ei ole vielä havaittu. Löydätkö ensimmäisen lajin?</p>"
    
    # taxa from json to dict
    my_taxa = dict()

    # If participant has own taxa, load them here
    if taxa_json:
        my_taxa = json.loads(taxa_json)

    # Ordinary challenger: all taxa file    
    if challenge_data["type"] == "challenge100":
        taxon_names = load_taxon_file(taxon_id + "_all")
    # School challenge: only basic taxa file
    elif challenge_data["type"] == "school100":
        taxon_names = load_taxon_file(taxon_id)
    else:
        raise ValueError("Unknown challenge type")
    
    number_of_participations = len(participations)

    taxa_counts = dict()
    for participation in participations:
        # Get taxa dict from taxa_json field
        taxa = json.loads(participation["taxa_json"])
        
        for taxon_id, date in taxa.items():
            if taxon_id not in taxa_counts:
                taxa_counts[taxon_id] = 0
            taxa_counts[taxon_id] += 1

    # Sort taxa by count
    taxa_counts_sorted = sorted(taxa_counts.items(), key=lambda x: x[1], reverse=True)
    number_of_taxa = len(taxa_counts_sorted)

    html = f"<p>Osallistujat ovat havainneet yhteensä { number_of_taxa } lajia.</p>"
    html += "<div class='table-container'>\n<table id='taxa_results'>"
    html += "<tr><th>Laji</th><th>Havaintoja</th><th>%</th></tr>"
    for taxon_id, count in taxa_counts_sorted:
        taxon_observed_class = "not_observed" # default
        taxon_observed_checkmark = ""
        if taxon_id in my_taxa:
            taxon_observed_class = "observed"
            taxon_observed_checkmark = "✅"

        # Check if taxon exists in all_taxa_names. Might not if it has been added to Laji.fi after the taxon list on this app has been set up.
        fin = "" # default
        swe = "" # default
        sci = taxon_id # default
        if taxon_id in taxon_names:
            sci = taxon_names[taxon_id]["sci"]
            # Finnish name might not exist
            if "fin" in taxon_names[taxon_id]:
                fin = taxon_names[taxon_id]["fin"].capitalize()
            # Swedish name might not exist
            if "swe" in taxon_names[taxon_id]:
                swe = taxon_names[taxon_id]["swe"]


        html += f"<tr class='{ taxon_observed_class }'>"
        html += f"<td>{ fin }, { swe } <em>({ sci })</em> { taxon_observed_checkmark }</td>"
        html += f"<td>{ count }</td>"
        html += f"<td>{ str(round(((count / number_of_participations) * 100), 1)).replace('.', ',') } %</td>"
        html += "</tr>"

    html += "</table>\n</div>"
    
    return html


# Function to calculate how many participants have reached at least a given proportion or number of taxa
def get_participant_count(participations, target_count):

    '''
    # Proportion, UNTESTED
    proportion = 0.1
    count = 0
    for participation in participations:
        if participation["taxa_count"] >= target_count * proportion:
            count += 1
    '''

    # Number
    count = 0
    for participation in participations:
        if participation["taxa_count"] >= target_count:
            count += 1

    return count

# Function to format a pair of dates to Finnish date format
def date_to_fi(date_begin, date_end):
    date_begin_parts = date_begin.split("-")
    date_end_parts = date_end.split("-")

    # Check if whole year
    if date_begin_parts[1] == "01" and date_begin_parts[2] == "01" and date_end_parts[1] == "12" and date_end_parts[2] == "31":
        return f"koko vuosi { date_begin_parts[0] }"

    # Else return formatted date range
    return f"{ date_begin_parts[2] }.{ date_begin_parts[1] }.{ date_begin_parts[0] } &ndash; { date_end_parts[2] }.{ date_end_parts[1] }.{ date_end_parts[0] }"


def make_safe_filename(original_string):
    # Replace spaces with underscores
    safe_string = original_string.replace(" ", "_")
    
    # Remove any character that is not a letter, number, underscore, or hyphen
    safe_string = re.sub(r'[^\w\-_]', '', safe_string)
    
    # Limit the length of the filename if necessary
    max_length = 255  # Adjust this limit as needed
    safe_string = safe_string[:max_length]
    
    return safe_string