from flask import g

def main():
    html = dict()
    html["hello"] = "Hoi "

    print("== home ==")
    print(g.token)
    print(g.user_data)

    return html