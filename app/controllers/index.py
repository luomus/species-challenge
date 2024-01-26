from flask import g
from helpers import common_db

def main():
    html = dict()
    html["hello"] = "Hoi "

    with common_db.connection() as conn:
        query = "SELECT * FROM challenges"
        data = common_db.select(conn, query)
        for row in data:
            print(row)

    print("== home ==")
    print(g.token)
    print(g.user_data)

    return html