from flask import Flask, render_template, redirect
import sys

import controllers.index

app = Flask(__name__)
#app.secret_key = app_secrets.flask_secret_key

print("-------------- BEGIN --------------", file = sys.stdout)

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')

@app.route("/")
def root():
    html = controllers.index.main()
    return render_template("index.html", html=html)
