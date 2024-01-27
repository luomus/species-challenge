# Common helpers functions.

import uuid
import requests
import json
import sys
import os

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


def clean_uuid(input_string):
    """
    Validates if a given string is a valid UUID.

    Args:
    input_string (str): The string to validate.

    Returns:
    str: The input_string if it is a valid UUID.

    Raises:
    ValueError: If the input_string is invalid as an UUID.
    """
    try:
        uuid.UUID(input_string, version=4)
    except ValueError:
        raise ValueError("UUID is not valid.")

    return input_string
