# Controller for a navigation page that displays my participations to challenges.

from flask import g
from helpers import common_db

def get_participations(status):
    params = (status, g.user_data["id"])
    with common_db.connection() as conn:
        query = """SELECT p.*, c.*
            FROM participations p
            JOIN challenges c ON p.challenge_id = c.challenge_id
            WHERE c.status = %s
            AND p.meta_created_by = %s;"""
        data = common_db.select(conn, query, params)
    return data


def make_participations_html(participations):
    html = ""
    for participation in participations:
        if not participation['taxa_count']:
            participation['taxa_count'] = 0

        html += f"<div class='participation'>\n"
        html += f"<h3>{ participation['title'] }</a></h3>\n"
        html += f"<p>{ participation['name'] }, { participation['place'] }</p>\n"
        html += f"<p>{ participation['taxa_count'] } lajia <a href='/osallistuminen/{ participation['challenge_id'] }/{ participation['participation_id'] }' class='button'>Muokkaa osallistumista</a></p>\n"
        html += "</div>\n"
    return html


def main():
    html = dict()

    print(get_participations("open"))

    html["open_participations"] = make_participations_html(get_participations("open"))
    html["draft_participations"] = make_participations_html(get_participations("draft"))
    html["closed_participations"] = make_participations_html(get_participations("closed"))

    return html