# Script to read Laji.fi name file and create a json file for this app.

"""
Input file format (tsv):
Scientific name	Identifier	Vernacular name	Finnish name	Swedish name	Observation count from Finland
Bangia atropurpurea	http://tun.fi/MX.292132	tyrskypurppuralanka (fi)	tyrskypurppuralanka		3
Rhodochorton purpureum	http://tun.fi/MX.254277	purppurasamettilevä (fi)	purppurasamettilevä		645
Ceramium tenuicorne	http://tun.fi/MX.206699	punahelmilevä (fi)	punahelmilevä	röd havsmossa	13178

Output file format (json):
{
 "MX.292132": {
  "fin": "tyrskypurppuralanka",
  "sci": "Bangia atropurpurea",
  "swe": ""
 },
 "MX.254277": {
  "fin": "purppurasamettilevä",
  "sci": "Rhodochorton purpureum",
  "swe": ""
 },
 "MX.206699": {
  "fin": "punahelmilevä",
  "sci": "Ceramium tenuicorne",
  "swe": "röd havsmossa"
 },
"""

import pandas as pd
import json

input_filename = "fungi.tsv"
output_filename = "fungi_2025_all.json"

# Read the tsv file
df = pd.read_csv(input_filename, sep='\t', header=0)

# Convert NaN to empty string
df = df.fillna('')

# For Identifier, remove the http://tun.fi/ part
df['Identifier'] = df['Identifier'].str.replace('http://tun.fi/', '')

# Convert 'Observation count from Finland' to numeric, replacing empty strings with 0
df['Observation count from Finland'] = pd.to_numeric(df['Observation count from Finland'].replace('', '0'), errors='coerce').fillna(0).astype(int)

# Sort by observation count descending
df = df.sort_values('Observation count from Finland', ascending=False)

print(df.head())

# Replace column names as "fin", "sci", "swe"
df.rename(columns={'Finnish name': 'fin', 'Swedish name': 'swe', 'Scientific name': 'sci'}, inplace=True)

# Remove all other columns
df = df[['Identifier', 'fin', 'sci', 'swe']]

# Create a dictionary where Identifier is the key
data = df.set_index('Identifier').to_dict(orient='index')

# Add exceptional names

# Plantae
exceptional_names = {
    "MX.42419": {
        "fin": "voikukat",
        "sci": "Taraxacum",
        "swe": "maskrosor"
    }
}

# Fungi
exceptional_names = {
    "MX.69690": {
        "fin": "mesisienet",
        "sci": "Armillaria",
        "swe": ""
    },
    "MX.5019989": {
        "fin": "veriseitikkiryhmä",
        "sci": "Cortinarius sanguineus coll.",
        "swe": ""
    },
    "MX.72871": {
        "fin": "verihelttaseitikkiryhmä",
        "sci": "Cortinarius semisanguineus coll.",
        "swe": ""
    },
    "MX.72622": {
        "fin": "valkorisakasryhmä",
        "sci": "Inocybe geophylla coll.",
        "swe": "sidentråding"
    },
    "MX.72524": {
        "fin": "pulkkosieniryhmä",
        "sci": "Paxillus involutus coll.",
        "swe": ""
    },
    "MX.5102924": {
        "fin": "punikkitatit",
        "sci": "Leccinum versipelle group.",
        "swe": ""
    },
    "MX.205986": {
        "fin": "rusko-orakasryhmä",
        "sci": "Hydnum rufescens coll.",
        "swe": ""
    },
    "MX.5102921": {
        "fin": "kuusensuomu-/männynsuomuorakas",
        "sci": "Sarcodon imbricatus/squamosus",
        "swe": ""
    },
    "MX.237062": {
        "fin": "mustamörskyryhmä",
        "sci": "Helvella lacunosa coll.",
        "swe": ""
    },
    "MX.5076303": {
        "fin": "piispanhiipparyhmä",
        "sci": "Gyromitra infula coll.",
        "swe": ""
    },
    "MX.67279": {
        "fin": "tummalupot",
        "sci": "Bryoria",
        "swe": "tagellavar"
    },
    "MX.67190": {
        "fin": "kehräjäkälät",
        "sci": "Lecanora",
        "swe": "kantlavar"
    },
    "MX.67052": {
        "fin": "tinajäkälät",
        "sci": "Stereocaulon",
        "swe": "påskrislavar"
    },
    "MX.67212": {
        "fin": "naavat",
        "sci": "Usnea",
        "swe": "skägglavar"
    }
}


# Update the data dictionary with exceptional names (they will appear first)
data = {**exceptional_names, **data}

#print(data)

# Save the data to a json file
with open(output_filename, 'w') as f:
    json.dump(data, f, indent=1)

print(f"Data saved to { output_filename }")