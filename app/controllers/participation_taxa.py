# Controller for a page that lists all taxa for a single participation.

from helpers import common_helpers
from datetime import datetime
import json

def main(challenge_id_untrusted, participation_id_untrusted):
    html = dict()

    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

    html["challenge_id"] = challenge_id
    html["participation_id"] = participation_id

    challenge_data = common_helpers.get_challenge(challenge_id)
    participation_data = common_helpers.get_participation(challenge_id, participation_id)

    taxa_names = common_helpers.load_taxon_file(challenge_data['taxon'] + "_all")

    if not participation_data:
        # Not participation of this user
        return {"redirect": True, "url": "/"}

    html["challenge_data"] = challenge_data
    html["participation_data"] = participation_data
#    print(taxa_names)

    # Generate taxon rows
    # Convert participation_data["taxa_json"] to dict
    participation_dict = json.loads(participation_data["taxa_json"])

    # Loop participation_data["taxa_json"], which contains observed taxon codes and dates
    html["taxa_html"] = "<div class='table-container'>\n<table id='taxa'>\n<thead>\n<tr>\n<th>Suomenkielinen nimi</th><th>Ruotsinkielinen nimi</th><th>Tieteellinen nimi</th><th>Havaintopäivämäärä</th>\n</tr>\n</thead>\n<tbody>\n"

    for taxon_id, date in participation_dict.items():
        # Skip if taxon not found, can happen if taxon list is changed after the challenge has been created
        if not taxon_id in taxa_names:
            continue
        fin_name = taxa_names[taxon_id].get('fin', "")
        swe_name = taxa_names[taxon_id].get('swe', "")
        sci_name = taxa_names[taxon_id].get('sci', "")
        full_taxon_id = f"http://tun.fi/{taxon_id}"

        row = f"<tr><td>{fin_name}</td><td>{swe_name}</td><td><em>{sci_name}</em></td><td>{date}</td></tr>\n"
        html["taxa_html"] += row

    html["taxa_html"] += "</tbody>\n</table>\n</div>\n"
    return html
