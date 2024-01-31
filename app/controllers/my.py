# Controller for a navigation page that displays my participations to challenges.

from flask import g
from helpers import common_db

def get_participations(status, trashed):
    if status == "all":
        params = (g.user_data["id"], trashed)
        with common_db.connection() as conn:
            query = """SELECT p.*, c.*
                FROM participations p
                JOIN challenges c ON p.challenge_id = c.challenge_id
                WHERE p.meta_created_by = %s
                AND p.trashed = %s
            ;"""
            data = common_db.select(conn, query, params)
    else:
        params = (status, g.user_data["id"], trashed)
        with common_db.connection() as conn:
            query = """SELECT p.*, c.*
                FROM participations p
                JOIN challenges c ON p.challenge_id = c.challenge_id
                WHERE c.status = %s
                AND p.meta_created_by = %s
                AND p.trashed = %s
            ;"""
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

    html["open_participations"] = make_participations_html(get_participations("open", 0))
    html["draft_participations"] = make_participations_html(get_participations("draft", 0))
    html["closed_participations"] = make_participations_html(get_participations("closed", 0))
    html["trashed_participations"] = make_participations_html(get_participations("all", 1))

    return html