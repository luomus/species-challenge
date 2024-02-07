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
    if "access_token=" not in api_url:
        print("WARNING: access_token param is missing from your url!", file = sys.stdout)

    api_url = api_url + os.environ.get('FINBIF_API_TOKEN')
    print("Fetching API: " + api_url, file = sys.stdout)

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
    print("Fetching API: " + api_url, file = sys.stdout)

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


def is_year(input_string):
    """
    Validates if a given string is a valid year in YYYY format.

    Args:
    input_string (str): The string to validate.

    Returns:
    bool: True if the input_string is a valid year in YYYY format,
    False otherwise.
    """
    pattern = re.compile(r'^\d{4}$')
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
    Checks if a file exists in ./data/{taxon_file_id}.json.

    Args:
    taxon_file_id (str): The taxon file id (from database).

    Returns:
    bool: True if the file exists, False otherwise.
    """
    filename = "./data/" + taxon_file_id + ".json"
    return os.path.isfile(filename)


def load_taxon_file(taxon_file_id):
    """
    Loads a taxon file from ./data/{taxon_file_id}.json.

    Args:
    taxon_id (str): The taxon file id (from database).

    Returns:
    dict: A dictionary containing the taxon file data.
    """
    file_path = f"./data/{ taxon_file_id }.json"
    with open(file_path, 'r') as file:
        taxa_names = json.load(file)

    return taxa_names



def get_challenge(challenge_id):
    params = (challenge_id,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE challenge_id = %s"
        data = common_db.select(conn, query, params)
    return data[0]


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


def make_taxa_html(participations, taxon_id, taxa_json = ""):
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
    if taxa_json:
        my_taxa = json.loads(taxa_json)
    
    taxon_names = load_taxon_file(taxon_id + "_all")
    
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
    html += "<table id='taxa_results'>"
    html += "<tr><th>Laji</th><th>Havaintoja</th><th>%</th></tr>"
    for taxon_id, count in taxa_counts_sorted:
        taxon_observed_class = "not_observed" # default
        taxon_observed_checkmark = ""
        if taxon_id in my_taxa:
            taxon_observed_class = "observed"
            taxon_observed_checkmark = "✅"

        html += f"<tr class='{ taxon_observed_class }'>"
        html += f"<td>{ taxon_names[taxon_id]['fi'] } <em>({ taxon_names[taxon_id]['sci'] })</em> { taxon_observed_checkmark }</td>"
        html += f"<td>{ count }</td>"
        html += f"<td>{ str(round(((count / number_of_participations) * 100), 1)).replace('.', ',') } %</td>"
        html += "</tr>"

    html += "</table>"
    
    return html
