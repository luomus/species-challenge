# Controller for a page that displays a single participation and statistics about it.

from helpers import common_db
from helpers import common_helpers


def main(challenge_id_untrusted, participation_id_untrusted):
    html = dict()

    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    participation_id = common_helpers.clean_int(participation_id_untrusted)

    challenge_data = common_helpers.get_challenge(challenge_id)
    participations = common_helpers.get_all_participations(challenge_id)

    participation_data = common_helpers.get_participation(challenge_id, participation_id)
    if not participation_data:
        # Not participation of this user
        return {"redirect": True, "url": "/"}

    html["taxa_html"] = common_helpers.make_taxa_html(participations, challenge_data, participation_data["taxa_json"])

    html["challenge_data"] = challenge_data
    html["participation_data"] = participation_data
    html["challenge_id"] = challenge_id
    html["participation_id"] = participation_id

    return html