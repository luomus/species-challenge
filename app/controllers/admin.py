# Controller for administration page that displays challenges, statistics and options to edit them.

from flask import g
from helpers import common_db
import datetime

def get_challenges(status):
    params = (status,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE status LIKE %s ORDER BY year ASC"
        data = common_db.select(conn, query, params)
    return data


def make_challenges_html(challenges):
    html = ""
    for challenge in challenges:
        html += "<div class='challenge'>\n"
        html += f"<h4>{ challenge['title'] }</a></h4>\n"
        html += f"<p>{ challenge['year'] }, <a href='https://laji.fi/taxon/{ challenge['taxon'] }' target='_blank'>{ challenge['taxon'] }</a></p>\n"
        html += f"<p><a href='/haaste/{ challenge['challenge_id'] }' class='button'>Muokkaa</a></p>\n"
        html += "</div>\n"
    return html


def main():
    html = dict()

    html["open_challenges"] = make_challenges_html(get_challenges("open"))
    html["draft_challenges"] = make_challenges_html(get_challenges("draft"))
    html["closed_challenges"] = make_challenges_html(get_challenges("closed"))


    return html