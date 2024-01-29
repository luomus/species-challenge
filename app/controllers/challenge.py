# Controller for a page that displays a single challenge and statistics about it.

from flask import g, flash
from helpers import common_db
from helpers import common_helpers

def get_challenge(challenge_id):
    params = (challenge_id,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE challenge_id = %s"
        data = common_db.select(conn, query, params)
    return data[0]


def make_challenge_html(challenge):
    html = ""
    return html


def main(challenge_id_untrusted):
    html = dict()

    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    if not challenge_id:
        raise ValueError
    
    challenge_data = get_challenge(challenge_id)
    if not challenge_data:
        flash("Tätä haastetta ei löydy.", "info")
        return {"redirect": True, "url": "/"}

    print(challenge_data)
    html["challenge_info"] = make_challenge_html(challenge_data)


    return html