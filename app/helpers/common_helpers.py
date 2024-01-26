import requests
import json
import sys
import os

def fetch_finbif_api(api_url, log = False):
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

    dataJson = r.text
    dataDict = json.loads(dataJson)

    if "status" in dataDict:
        if 403 == dataDict["status"]:
            print("ERROR: api.laji.fi 403 error.", file = sys.stdout)
            raise ConnectionError

    return dataDict