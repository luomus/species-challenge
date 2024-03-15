# Controller for a page that displays a single challenge, my participations and statistics about it.

from flask import g, flash
from helpers import common_db
from helpers import common_helpers


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


def make_participant_html(participations):
    if not participations:
        return "<p>Kukaan ei ole vielä osallistunut tähän haasteeseen. Oletko ensimmäinen?</p>"

    html = ""
    table = ""

    table += "<table id='participant_results'>"
    table += "<tr><th>Osallistuja</th><th>Paikka</th><th>Lajimäärä</th></tr>"

    target_count = 100
    target_taxa_count_reached = 0
    taxa_count_total = 0

    # Table of participants: name, place, taxon_count
    for participation in participations:
        name_shown = ""
        if participation["taxa_count"] >= target_count:
            name_shown = participation['name']

        table += "<tr>"
        table += f"<td>{ name_shown }</td>"
        table += f"<td>{ participation['place'] }</td>"
        table += f"<td>{ participation['taxa_count'] }</td>"
        table += "</tr>"

        taxa_count_total = taxa_count_total + participation["taxa_count"]
        if participation["taxa_count"] >= target_count:
            target_taxa_count_reached += 1
    
    table += "</table>"

    number_of_participants = len(participations)
    target_taxa_count_reached_percent = round(target_taxa_count_reached / number_of_participants * 100, 1)
    taxa_count_average = round(taxa_count_total / number_of_participants, 1)

    html += f"<p>Haasteessa on { number_of_participants } osallistujaa, joista { target_taxa_count_reached } ({ str(target_taxa_count_reached_percent).replace('.', ',') } %) on saavuttanut tavoitteen ({ target_count } lajia). Keskimäärin osallistujat ovat havainneet { str(taxa_count_average).replace('.', ',') } lajia.</p>"
    html += f"<p>Osallistujien nimet tulevat näkyviin, kun he ovat havainneet 100 lajia.</p></p>"

    html += table 
    return html


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


def main(challenge_id_untrusted):
    html = dict()

    # Check input validity
    challenge_id = common_helpers.clean_int(challenge_id_untrusted)
    if not challenge_id:
        raise ValueError

    print("Log: ", challenge_id)

    challenge_data = common_helpers.get_challenge(challenge_id)
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
    participations = common_helpers.get_all_participations(challenge_id)
    html["participant_html"] = make_participant_html(participations)

    html["taxa_html"] = common_helpers.make_taxa_html(participations, challenge_data["taxon"])

    return html
