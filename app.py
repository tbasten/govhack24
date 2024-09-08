import flask
from flask import render_template, redirect, url_for
import pandas as pd
from collections import defaultdict
import json


app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = True

sensor_map = {
    "Mary Cairncross Scenic Reserve": {
        "BBQ_East": {
            "temp": [
                "r718b140-06f8"
                "r718b140-06fc"
                "r718b140-06f9"
            ]
        },
        "BBQ_West": {
            "temp": [
                "r718b140-06f7"
                "r718b140-06fa"
            ]
        }
    }
}


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/admin")
def admin():
    return redirect(url_for("home"))

df = pd.read_csv('data/r718b140-06f7-BBQ Temp.csv')

for i in df:
    print(i)

if __name__ == '__main__':
    app.run(host="localhost", port=80, debug=True)