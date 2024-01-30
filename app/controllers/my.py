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

'''
Data from the above query looks like this:

[{'participation_id': 5, 'challenge_id': 4, 'name': 'Nimi Merkkinen', 'place': 'Nimismiehenkylä', 'taxa_count': 0, 'taxa_json': '{}', 'meta_created_by': 'MA.3', 'meta_created_at': datetime.datetime(2024, 1, 28, 10, 42, 23), 'meta_edited_by': 'MA.3', 'meta_edited_at': datetime.datetime(2024, 1, 30, 15, 48, 43), 'taxon': 'MX.53078', 'year': 2024, 'type': 'challenge100', 'title': 'Putkilokasvit 2024 D', 'status': 'open', 'description': 'Foo bar'}, {'participation_id': 6, 'challenge_id': 4, 'name': "André D'Artágnan", 'place': 'Ääkkölä ääkkölärules', 'taxa_count': 6, 'taxa_json': '{"MX.37691": "2024-01-11", "MX.37721": "2024-01-02", "MX.37717": "2024-01-27", "MX.37719": "2024-01-28", "MX.37763": "2024-01-10", "MX.37771": "2024-01-18"}', 'meta_created_by': 'MA.3', 'meta_created_at': datetime.datetime(2024, 1, 28, 10, 42, 23), 'meta_edited_by': 'MA.3', 'meta_edited_at': datetime.datetime(2024, 1, 30, 15, 48, 43), 'taxon': 'MX.53078', 'year': 2024, 'type': 'challenge100', 'title': 'Putkilokasvit 2024 D', 'status': 'open', 'description': 'Foo bar'}, {'participation_id': 7, 'challenge_id': 5, 'name': 'Foo', 'place': 'Bar', 'taxa_count': 0, 'taxa_json': '{}', 'meta_created_by': 'MA.3', 'meta_created_at': datetime.datetime(2024, 1, 28, 22, 32, 58), 'meta_edited_by': 'MA.3', 'meta_edited_at': datetime.datetime(2024, 1, 28, 22, 32, 58), 'taxon': 'MX.53078', 'year': 2024, 'type': 'challenge100', 'title': 'sdf', 'status': 'open', 'description': ''}, {'participation_id': 8, 'challenge_id': 4, 'name': 'Foo', 'place': 'Bar', 'taxa_count': 0, 'taxa_json': '{}', 'meta_created_by': 'MA.3', 'meta_created_at': datetime.datetime(2024, 1, 28, 10, 42, 23), 'meta_edited_by': 'MA.3', 'meta_edited_at': datetime.datetime(2024, 1, 30, 15, 48, 43), 'taxon': 'MX.53078', 'year': 2024, 'type': 'challenge100', 'title': 'Putkilokasvit 2024 D', 'status': 'open', 'description': 'Foo bar'}]
'''

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