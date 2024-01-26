from flask import Flask, render_template, redirect
import sys
import os

import controllers.index

app = Flask(__name__)

# Get secret key from environment variables, stop if not found.
secret_key = os.environ.get('FLASK_SECRET_KEY')
if secret_key is None:
    raise ValueError("No FLASK_SECRET_KEY set.")
app.secret_key = secret_key

print("-------------- BEGIN --------------", file = sys.stdout)

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')

@app.route("/")
def root():
    html = controllers.index.main()
    return render_template("index.html", html=html)
