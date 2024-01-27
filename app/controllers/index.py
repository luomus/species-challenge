# Controller for the front page that displays open and closed challenges.

from flask import g
from helpers import common_db
import datetime

def get_open_challenges():
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE status = 'open'"
        data = common_db.select(conn, query)
    return data


def make_challenges_html(challenges):
    html = "<ul>\n"
    for challenge in challenges:
        html += f"<li><a href='{ challenge['id'] }'>{ challenge['name'] }</a></li>\n"
    html += "</ul>\n"
    return html


def main():
    html = dict()
    html["hello"] = "Hoi "

    challenges = get_open_challenges()
    html["challenges"] = make_challenges_html(challenges)

    print("== home ==")
    print(g.token)
    print(g.user_data)

    return html