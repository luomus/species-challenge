# Controller for a page that displays a single challenge, my participations and statistics about it.

from flask import g, flash
from helpers import common_db
from helpers import common_helpers
import json

def get_challenge(challenge_id):
    params = (challenge_id,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE challenge_id = %s"
        data = common_db.select(conn, query, params)
    return data[0]


def make_challenge_html(challenge):
    html = "<div id='challenge_info'>"

    html += "<h1>" + challenge["title"] + "</h1>"
    html += "<p>" + str(challenge["description"]) + "</p>"
    if challenge["status"] == "open":
        html += "<p><strong>Tämä haaste on avoinna, tervetuloa osallistumaan!</strong></p>"
    if challenge["status"] == "closed":
        html += "<p><strong>Tämä haaste on loppunut.</strong> <a href='/'>Tutustu muihin käynnissä oleviin haasteisiin!</a></p>"

    html += "</div>"
    return html


# Function to get participations of current user to this challenge, excluding trashed participations
def get_my_participations(challenge_id):
    with common_db.connection() as conn:
        query = "SELECT * FROM participations WHERE challenge_id = %s AND meta_created_by = %s AND trashed = 0"
        params = (challenge_id, g.user_data["id"])
        participations = common_db.select(conn, query, params)

    return participations


def make_participations_html(participations, challenge_id, challenge_status):
    html = ""
    for participation in participations:
        html += "<li>"
        html += "<a href='/osallistuminen/" + str(participation["challenge_id"]) + "/" + str(participation["participation_id"]) + "'>"
        html += ", ".join([participation["name"], participation["place"]])
        html += "</a>"
        html += "</li>"

    if html:
        html = f"<ul>\n{ html }\n</ul>"
        if challenge_status == "open":
            html += f"<a href='/osallistuminen/{ challenge_id }' class='button' id='add_participation'>Lisää uusi osallistuminen</a></p>"
    else:
        html = "<p>Et ole osallistunut tähän haasteeseen.</p>"
        if challenge_status == "open":
            html += f"<p><a href='/osallistuminen/{ challenge_id }' class='button' id='add_participation'>Osallistu</a></p>"

    return html


def make_taxa_html(participations, taxon_id):
    '''
    participations -variable contains data like this:
    [
        {
            'participation_id': 5, 
            'challenge_id': 4, 
            'name': 
            'Nimi Merkkinen', 'place': 
            'Nimismiehenkylä', 'taxa_count': 28, 
            'taxa_json': '{"MX.37691": "2024-01-30", "MX.37721": "2024-01-30", "MX.37717": "2024-01-17", "MX.37719": "2024-01-25", "MX.37763": "2024-01-01", "MX.37771": "2024-01-30", "MX.4994055": "2024-01-03", "MX.37752": "2024-01-30", "MX.37747": "2024-01-30", "MX.37826": "2024-01-30", "MX.37812": "2024-01-10", "MX.37819": "2024-01-30", "MX.40138": "2024-01-30", "MX.39201": "2024-01-30", "MX.39235": "2024-01-30", "MX.4973227": "2024-01-17", "MX.39887": "2024-01-30", "MX.39917": "2024-01-11", "MX.38279": "2024-01-02", "MX.38598": "2024-01-13", "MX.39052": "2024-01-20", "MX.39038": "2024-01-11", "MX.39465": "2024-01-18", "MX.39673": "2024-01-30", "MX.39967": "2024-01-30", "MX.38301": "2024-01-30", "MX.40632": "2024-01-11", "MX.38843": "2024-01-25"}', 
            'meta_created_by': 'MA.3', 
            'meta_created_at': datetime.datetime(2024, 1, 28, 15, 19, 17), 
            'meta_edited_by': 'MA.3', 
            'meta_edited_at': datetime.datetime(2024, 1, 31, 11, 37, 2), 
            'trashed': 0
        },
        {
            'participation_id': 6, 
            'challenge_id': 4, 
            'name': "André D'Artágnan", 
            'place': 'Ääkkölä ääkkölärules', 
            'taxa_count': 14, 
            'taxa_json': '{"MX.37691": "2024-01-11", "MX.37721": "2024-01-02", "MX.37717": "2024-01-27", "MX.37719": "2024-01-28", "MX.37763": "2024-01-10", "MX.37771": "2024-01-18", "MX.4994055": "2024-01-18", "MX.37752": "2024-01-30", "MX.40138": "2024-01-30", "MX.40150": "2024-01-30", "MX.39201": "2024-01-30", "MX.4973227": "2024-01-17", "MX.39827": "2024-01-25", "MX.39917": "2024-01-30"}', 
            'meta_created_by': 'MA.3', 
            'meta_created_at': datetime.datetime(2024, 1, 28, 15, 29, 1), 
            'meta_edited_by': 'MA.3', 
            'meta_edited_at': datetime.datetime(2024, 1, 31, 11, 34, 47), 
            'trashed': 0
        }
    ]
    '''
    if not participations:
        return "<p>Yhtään lajia ei ole vielä havaittu.</p>"
    
    taxon_names = common_helpers.load_taxon_file(taxon_id + "_all")
    
    number_of_participations = len(participations)

    taxa_counts = dict()
    for participation in participations:
        # Get taxa dict from taxa_jdon field
        taxa = json.loads(participation["taxa_json"])
        
        for taxon_id, date in taxa.items():
            if taxon_id not in taxa_counts:
                taxa_counts[taxon_id] = 0
            taxa_counts[taxon_id] += 1

    # Sort taxa by count
    taxa_counts_sorted = sorted(taxa_counts.items(), key=lambda x: x[1], reverse=True)
    number_of_taxa = len(taxa_counts_sorted)

    html = f"<p>Osallistujat ovat havainneet yhteensä { number_of_taxa } lajia.</p>"
    html += "<table id='taxa_results'>"
    html += "<tr><th>Laji</th><th>Havaintoja</th><th>%</th></tr>"
    for taxon_id, count in taxa_counts_sorted:
        html += "<tr>"
        html += f"<td>{ taxon_names[taxon_id]['fi'] } <em>({ taxon_names[taxon_id]['sci'] })</em></td>"
        html += f"<td>{ count }</td>"
        html += f"<td>{ str(round(((count / number_of_participations) * 100), 1)).replace('.', ',') } %</td>"
        html += "</tr>"

    html += "</table>"
    
    return html


def get_all_participations(challenge_id):
    with common_db.connection() as conn:
        query = "SELECT * FROM participations WHERE challenge_id = %s and trashed = 0 ORDER BY taxa_count DESC"
        params = (challenge_id,)
        participations = common_db.select(conn, query, params)

    return participations


def make_participant_html(participations):
    if not participations:
        return "<p>Kukaan ei ole vielä osallistunut tähän haasteeseen.</p>"

    html = ""
    table = ""

    table += "<table id='participant_results'>"
    table += "<tr><th>Osallistuja</th><th>Paikka</th><th>Lajimäärä</th></tr>"

    target_count = 10
    target_taxa_count_reached = 0
    taxa_count_total = 0

    # Table of participants: name, place, taxon_count
    for participation in participations:
        sparkles = ""
        if participation["taxa_count"] >= target_count:
            sparkles = "✨"

        table += "<tr>"
        table += f"<td>{ participation['name'] }</td>"
        table += f"<td>{ participation['place'] }</td>"
        table += f"<td>{ participation['taxa_count'] } { sparkles }</td>"
        table += "</tr>"

        taxa_count_total = taxa_count_total + participation["taxa_count"]
        if participation["taxa_count"] >= target_count:
            target_taxa_count_reached += 1
    
    table += "</table>"

    number_of_participants = len(participations)
    target_taxa_count_reached_percent = round(target_taxa_count_reached / number_of_participants * 100, 1)
    taxa_count_average = round(taxa_count_total / number_of_participants, 1)

    html += f"<p>Haasteessa on { number_of_participants } osallistujaa, joista { target_taxa_count_reached } ({ str(target_taxa_count_reached_percent).replace('.', ',') } % ) on savuttanut tavoitteen ({ target_count } lajia). Keskimäärin osallistujat ovat havainneet { str(taxa_count_average).replace('.', ',') } lajia.</p>"

    html += table 
    return html


def main(challenge_id_untrusted):
    html = dict()

    # Check input validity
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    if not challenge_id:
        raise ValueError
    
    challenge_data = get_challenge(challenge_id)
    if not challenge_data:
#        flash("Tätä haastetta ei löydy.", "info")
        return {"redirect": True, "url": "/"}
    
    # If challenge is still a draft, redirect to homepage
    if challenge_data["status"] == "draft":
#        flash("Tämä haaste ei ole juuri nyt avoinna.", "info")
        return {"redirect": True, "url": "/"}

    # Participation data
    # Logged in user
    if g.user_data:
        my_participations = get_my_participations(challenge_id)
        html["participations_html"] = make_participations_html(my_participations, challenge_id, challenge_data["status"])

    # Anonymous user
    else:
        html["participations_html"] = "<p><a href='/login'>Kirjaudu sisään</a> osallistuaksesi.</p>"

    # Challenge data
    html["challenge"] = challenge_data
    html["challenge_html"] = make_challenge_html(challenge_data)

    # Participation stats
    participations = get_all_participations(challenge_id)
    html["participant_html"] = make_participant_html(participations)

    html["taxa_html"] = make_taxa_html(participations, challenge_data["taxon"])

    return html