# Controller for a page that displays a single challenge, my participations and statistics about it.

from flask import g, flash
from helpers import common_db
from helpers import common_helpers


def make_challenge_html(challenge):
    html = "<div id='challenge_info'>"

    html += "<h1>" + challenge["title"] + "</h1>"
    html += "<p>" + str(challenge["description"]) + "</p>"
    html += "<p>Osallistumisaika: " + common_helpers.date_to_fi(challenge["date_begin"], challenge["date_end"]) + "</p>"

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
    table += "<tr><th>Osallistuja</th><th>Paikka</th><th>Lajimäärä</th>"
    if g.is_admin:
        table += "<th>Käyttäjä</th>"
        table += "<th>Lisätty</th>"
        table += "<th>Muokattu</th>"
    table += "</tr>"

    target_count = 100
    target_taxa_count_reached = 0
    taxa_count_total = 0

    # Table of participants: name, place, taxon_count
    for participation in participations:
        name_shown = ""

        # Show name if user has reached target count or is admin
        if participation["taxa_count"] >= target_count or g.is_admin:
            name_shown = participation['name']
        # Show name if user is logged in and is the creator of the participation
        elif g.user_data:
            if g.user_data["id"] == participation["meta_created_by"]:
                name_shown = f"{ participation['name'] } (sinä)"

        table += "<tr>"
        table += f"<td>{ name_shown }</td>"
        table += f"<td>{ participation['place'] }</td>"
        table += f"<td>{ participation['taxa_count'] }</td>"
        if g.is_admin:
            table += f"<td><a href='https://triplestore.luomus.fi/editor/{ participation['meta_created_by'] }' target='_blank'>{ participation['meta_created_by'] }</a></td>"
            table += f"<td>{ participation['meta_created_at'] }</td>"
            table += f"<td>{ participation['meta_edited_at'] }</td>"
        table += "</tr>"

        taxa_count_total = taxa_count_total + participation["taxa_count"]
        if participation["taxa_count"] >= target_count:
            target_taxa_count_reached += 1
    
    table += "</table>"

    number_of_participants = common_helpers.get_participant_count(participations, 1)

    # Avoid division by zero
    if number_of_participants > 0:
        taxa_count_average = round(taxa_count_total / number_of_participants, 1)
        target_taxa_count_reached_percent = round(target_taxa_count_reached / number_of_participants * 100, 1)
    else:
        taxa_count_average = 0
        target_taxa_count_reached_percent = 0


    html += f"<p>Haasteessa on { number_of_participants } osallistujaa, joista { target_taxa_count_reached } ({ str(target_taxa_count_reached_percent) } %) on saavuttanut tavoitteen ({ target_count } lajia). Keskimäärin osallistujat ovat havainneet { str(taxa_count_average) } lajia.</p>"

    if g.is_admin:
        html += f"<p>Ylläpitäjänä näet kaikkien nimet ja osallistumisten lisäys- ja muokkausajat. Muut näkevät vain vähintään { target_count } havainneiden nimet ilman aikoja.</p></p>"
    else:
        html += f"<p>Osallistujien nimet tulevat näkyviin, kun he ovat havainneet { target_count } lajia.</p></p>"

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
    
    challenge_data = common_helpers.get_challenge(challenge_id)
    # If challenge not found, quietly redirect to homepage
    if not challenge_data:
        return {"redirect": True, "url": "/"}
    
    # If challenge is still a draft, quietly redirect to homepage
    if challenge_data["status"] == "draft":
        return {"redirect": True, "url": "/"}
    
    # TODO: If challenge is not open anymore

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

    html["taxa_html"] = common_helpers.make_taxa_html(participations, challenge_data)

    return html
