# Controller for a tsv file download with a single participation data.

from helpers import common_helpers
from datetime import datetime
import json

def main(challenge_id_untrusted, participation_id_untrusted):
    data = dict()

    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

    challenge_data = common_helpers.get_challenge(challenge_id)
    participation_data = common_helpers.get_participation(challenge_id, participation_id)

    # Todo: different taxon file types?
    taxa_names = common_helpers.load_taxon_file(challenge_data['taxon'] + "_all")

    if not participation_data:
        # Not participation of this user
        return {"redirect": True, "url": "/"}

    print(challenge_data)
    print(participation_data)
#    print(taxa_names)

    data["tsv"] = "Suomenkielinen nimi\tRuotsinkielinen nimi\tTieteellinen nimi\tTaksonin tunniste\tHavaintopäivämäärä\tOsallistujan nimi\tOsallistumispaikan nimi\tOsallistumisen tunniste\tHaaste\tHaasteen tunniste\n"

    # Generate taxon rows
    # Convert participation_data["taxa_json"] to dict
    participation_dict = json.loads(participation_data["taxa_json"])

    # Loop participation_data["taxa_json"], which contains observed taxon codes and dates
    for taxon_id, date in participation_dict.items():
        # Skip if taxon not found, can happen if taxon list is changed after the challenge has been created
        if not taxon_id in taxa_names:
            continue
        fin_name = taxa_names[taxon_id].get('fin', "")
        swe_name = taxa_names[taxon_id].get('swe', "")
        sci_name = taxa_names[taxon_id].get('sci', "")
        full_taxon_id = f"http://tun.fi/{taxon_id}"

        row = f"{fin_name}\t{swe_name}\t{sci_name}\t{full_taxon_id}\t{date}\t{participation_data['name']}\t{participation_data['place']}\t{participation_data['participation_id']}\t{challenge_data['title']}\t{challenge_data['challenge_id']}\n"
        data["tsv"] += row


    # Unique filename for the download
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_title = common_helpers.make_safe_filename(challenge_data['title'])
    data['filename'] = f"{safe_title}_{current_datetime}.tsv"

    return data