from flask import g

def main(person_token_untrusted):

    print("=====")
    print(g.token)
    print(g.user_data)

    html = dict()
    html["hello"] = "Hello "
    return html