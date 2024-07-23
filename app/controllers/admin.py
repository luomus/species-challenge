# Controller for administration page that displays challenges, statistics and options to edit them.

from flask import g
from helpers import common_db
from helpers import common_helpers
import datetime

def get_challenges(status):
    params = (status,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE status = %s ORDER BY date_begin ASC"
        data = common_db.select(conn, query, params)
    return data


def get_participations(challenge_id):
    params = (challenge_id,)
    with common_db.connection() as conn:
        query = "SELECT * FROM participations WHERE challenge_id = %s and trashed = 0 ORDER BY taxa_count DESC"
        data = common_db.select(conn, query, params)
    return data


def make_participations_stats_html(participations):
    '''
    participations is like this:
    
     [{'participation_id': 6, 'challenge_id': 4, 'name': "André D'Artágnan", 'place': 'Ääkkölä ääkkölärules', 'taxa_count': 13, 'taxa_json': '{"MX.37691": "2024-01-11", "MX.37721": "2024-01-02", "MX.37717": "2024-01-27", "MX.37719": "2024-01-28", "MX.37763": "2024-01-10", "MX.37771": "2024-01-18", "MX.37752": "2024-01-30", "MX.40138": "2024-01-30", "MX.40150": "2024-01-30", "MX.39201": "2024-01-30", "MX.4973227": "2024-01-17", "MX.39827": "2024-01-25", "MX.39917": "2024-01-30"}', 'meta_created_by': 'MA.3', 'meta_created_at': datetime.datetime(2024, 1, 28, 15, 29, 1), 'meta_edited_by': 'MA.3', 'meta_edited_at': datetime.datetime(2024, 1, 31, 8, 5, 20), 'trashed': 0}, {'participation_id': 8, 'challenge_id': 4, 'name': 'Foo', 'place': 'Bar', 'taxa_count': 0, 'taxa_json': '{}', 'meta_created_by': 'MA.3', 'meta_created_at': datetime.datetime(2024, 1, 30, 15, 48, 29), 'meta_edited_by': 'MA.3', 'meta_edited_at': datetime.datetime(2024, 1, 30, 15, 48, 29), 'trashed': 0}]
    '''

    # Count number of participants that have N or more taxa_count, and count average taxa_count
    target_count = 100
    target_taxa_count_reached = 0
    taxa_count_total = 0

    number_of_participants = common_helpers.get_participant_count(participations, target_count)

    for participation in participations:
        if participation.get("taxa_count", 0) >= target_count:
            target_taxa_count_reached += 1
        taxa_count_total += participation["taxa_count"]

    # Avoid division by zero
    if number_of_participants > 0:
        taxa_count_average = round(taxa_count_total / number_of_participants, 1)
        target_taxa_count_reached_percent = round(target_taxa_count_reached / number_of_participants * 100, 1)
    else:
        taxa_count_average = 0
        target_taxa_count_reached_percent = 0

    html = "<div class='stats'>"
    html += f"{ target_count } lajia saavuttaneiden määrä: <strong>{ target_taxa_count_reached } / { number_of_participants } osallistujaa</strong> ({ str(target_taxa_count_reached_percent).replace('.', ',') } %)<br>"
    html += f"Keskimääräinen lajimäärä: { str(taxa_count_average).replace('.', ',') }"
    html += "</div>"

    return html


def make_challenges_html(challenges):
    html = ""
    for challenge in challenges:
        participations_html = ""

        if challenge["status"] == "open" or challenge["status"] == "closed":
            participations_html = "Ei osallistujia" # default value
            participations = get_participations(challenge["challenge_id"])
            if len(participations) > 0:
                participations_html = make_participations_stats_html(participations)

        html += "<div class='challenge'>\n"
        html += f"<h3>{ challenge['title'] }</a></h3>\n"
        html += participations_html
        html += "<p>"
        html += f"<a href='/admin/haaste/{ challenge['challenge_id'] }' class='button'>Muokkaa</a>"
        if challenge["status"] != "draft":
            html += f"<a href='/haaste/{ challenge['challenge_id'] }'>Haasteen etusivu</a>"
        html += "</p>\n"
        html += "</div>\n"
    return html


def main():
    html = dict()

    html["open_challenges"] = make_challenges_html(get_challenges("open"))
    html["draft_challenges"] = make_challenges_html(get_challenges("draft"))
    html["closed_challenges"] = make_challenges_html(get_challenges("closed"))


    return html