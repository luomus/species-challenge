# Common helpers functions.

import requests
import json
import sys
import os
import re


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

