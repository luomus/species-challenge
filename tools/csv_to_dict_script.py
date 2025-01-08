# Script to convert a CSV file from project coordinator to a json file for this app.
# Note: this is made for format in fall 2024

import pandas as pd

def csv_to_dict(file_path, id = 'id'):
    """
    Converts a CSV file to a dictionary.
    Uses the 'id' column as keys and the remaining columns as values.
    """
    # Read the CSV file with the correct delimiter
    data = pd.read_csv(file_path, delimiter=';')

    # Convert to dictionary
    data_dict = data.set_index(id).T.to_dict()

    return data_dict

input_file = "100lajia_lastenlista.csv"
output_file = input_file.replace(".csv", ".json")

species_dict = csv_to_dict(input_file, "mx")

# Make a new dictionary from species_dict, with these changes:
# Rename "fi" to "fin"
# Leave out "taso" and "Eliöryhmä"
# If a value is missing (nan), replace it with empty string 

new_species_dict = {}
for key, value in species_dict.items():
    new_value = {}
    for k, v in value.items():
        if k == "fi":
            new_value["fin"] = v
        elif k != "taso" and k != "Eliöryhmä":
            if pd.isna(v):
                new_value[k] = ""
            else:
                new_value[k] = v
    new_species_dict[key] = new_value

print(new_species_dict)

# Save as json
import json
with open(output_file, "w") as f:
    json.dump(new_species_dict, f, indent=1)
