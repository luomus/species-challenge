# Controller for the front page that displays open and closed challenges.

from flask import g
from helpers import common_db
import datetime

def get_challenges(status):
    params = (status,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE status = %s ORDER BY date_begin DESC"
        data = common_db.select(conn, query, params)
    return data


def make_challenges_html(challenges):
    html = ""
    for challenge in challenges:
        html += "<div class='challenge'>\n"
        html += f"<h3><a href='/haaste/{ challenge['challenge_id'] }'>{ challenge['title'] }</a></h3>\n"
        html += f"<div>{ challenge['description'] }</div>\n"
        html += "</div>\n"
    return html


def main():
    html = dict()

    html["open_challenges"] = make_challenges_html(get_challenges("open"))
    html["closed_challenges"] = make_challenges_html(get_challenges("closed"))

    return html
