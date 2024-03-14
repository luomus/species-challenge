
from helpers import common_db
from helpers import common_helpers

def get_challenge_taxa():
    with common_db.connection() as conn:
        query = "SELECT taxon FROM challenges GROUP BY taxon"
        return common_db.select(conn, query)


def main():
    errors = ""

    # Database connection
    try:
        challenge_taxa = get_challenge_taxa()
    except Exception as e:
        errors += "Database error"
        return errors

    # Check that the taxon files exist
    for element in challenge_taxa:

        # Check that the taxon file exists
        if not common_helpers.taxon_file_exists(element["taxon"]):
            errors += f"Taxon file {element['taxon']} does not exist.\n"

    return errors