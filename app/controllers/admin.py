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
    html = "<div class='challenge'>\n"
    for challenge in challenges:
        html += f"<h4>{ challenge['name'] }</a></h4>\n"
        html += f"<p>{ challenge['year'] }</p>\n"
        html += f"<p><a href='/edit_challenge{ challenge['id'] }' class='button'>Muokkaa</a></p>\n"
    html += "</div>\n"
    return html


def main():
    html = dict()

    open_challenges = get_challenges("open")
    html["open_challenges"] = make_challenges_html(open_challenges)

    return html