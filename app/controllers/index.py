from flask import g
from helpers import common_db


def get_challenges(year):
    params = (year,)
    with common_db.connection() as conn:
        query = "SELECT * FROM challenges WHERE year = %s"
        data = common_db.select(conn, query, params)
    print(data)
    return data


def main():
    html = dict()
    html["hello"] = "Hoi "

    challenges = get_challenges(2024)

    print("== home ==")
    print(g.token)
    print(g.user_data)

    return html