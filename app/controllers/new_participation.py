# Controller for a form to submit new participation to a challenge.
# Available for logged in users.

from flask import g
from helpers import common_db


def main():
    html = dict()

    print(g.token)
    print(g.user_data)

    return html