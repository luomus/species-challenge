# Controller for a page that displays a single challenge, my participations and statistics about it.

from flask import g, flash
from helpers import common_db
from helpers import common_helpers

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
def get_participations(challenge_id):
    with common_db.connection() as conn:
        query = "SELECT * FROM participations WHERE challenge_id = %s AND meta_created_by = %s AND trashed = 0)"
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
        html = f"<h2>Osallistumiseni</h2>\n<ul>\n{ html }\n</ul>"
        if challenge_status == "open":
            html += f"<a href='/osallistuminen/{ challenge_id }' class='button'>Lisää uusi osallistuminen</a></p>"
    else:
        html = "<p>Et ole osallistunut tähän haasteeseen.</p>"
        if challenge_status == "open":
            html += f"<a href='/osallistuminen/{ challenge_id }' class='button'>Osallistu</a></p>"

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
        my_participations = get_participations(challenge_id)
        html["participations_html"] = make_participations_html(my_participations, challenge_id, challenge_data["status"])

    # Anonymous user
    else:
        html["participations_html"] = "<a href='/login'>Kirjaudu sisään</a> osallistuaksesi.</p>"


    # Challenge data
    print(challenge_data)
    html["challenge"] = challenge_data
    html["challenge_html"] = make_challenge_html(challenge_data)


    return html