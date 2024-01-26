from flask import g
from helpers import common_db


def get_challenges(year):
    params = (year,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE year = %s"
        data = common_db.select(conn, query, params)
    return data


def create_challenges_html(challenges):
    html = "<ul>\n"
    for challenge in challenges:
        html += f"<li><a href='{ challenge['id'] }'>{ challenge['name'] }</a></li>\n"
    html += "</ul>\n"
    return html


def main():
    html = dict()
    html["hello"] = "Hoi "

    challenges = get_challenges(2024)
    html["challenges"] = create_challenges_html(challenges)

    print("== home ==")
    print(g.token)
    print(g.user_data)

    return html