# Script to fetch species names from FinBIF API and update the species names in the species list
# This was used to update names after challenge 2024 had already started.

import requests
import json
import time

'''
{
 "MX.71896": {
  "sci": "Agaricus sylvicola",
  "fin": "kuusiherkkusieni",
  "heading": "Helttasienet",
  "swe": "knölchampinjon"
 },
 "MX.71663": {
  "sci": "Amanita crocea",
  "fin": "oranssikärpässieni",
  "swe": "orange kamskivling"
 },
'''

# Read json file, with species as a list of dictionaries (structure example above)

input_filename = 'fungi_2024.json'
output_filename = input_filename.split('.')[0] + '_updated.json'

token = "ADD TOKEN HERE"

with open(input_filename) as f:
    species_data = json.load(f)

# Loop the species
i = 0
for id, s in species_data.items():
    # If "swe" is missing or empty, fetch the species name from FinBIF API
    if not s.get('swe'):
        url = f"https://api.laji.fi/v0/taxa/{ id }?lang=multi&langFallback=true&maxLevel=0&includeHidden=false&includeMedia=false&includeDescriptions=false&includeRedListEvaluations=false&sortOrder=taxonomic&access_token={ token }"
        response = requests.get(url)
        data = response.json()
        # Update the species name in the species list
        # First check that swedish name exists
        if data.get('vernacularName') and data['vernacularName'].get('sv'):
            s['swe'] = data['vernacularName']['sv']
            print("- Swedish name updated: ", id, s['swe'])
            i += 1
        else:
            print("Swedish name not found for: ", s['sci'])

        time.sleep(1)
    else:
        print("Swedish name already exists: ", s['swe'])

# Save the updated species list
with open(output_filename, 'w') as f:
    json.dump(species_data, f, indent=1)

print(f"{ i } names updated and saved to { output_filename }")

