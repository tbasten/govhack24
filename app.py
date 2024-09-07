import flask
from flask import render_template, redirect, url_for
import pandas as pd
from collections import defaultdict
import json


app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = True



@app.route("/")
def home():
    return render_template("home.html")
@app.route("/admin")
def admin():
    return redirect(url_for("home"))

df = pd.read_csv('data/r718b140-06f7-BBQ Temp.csv')
grouped_data = df.groupby('dev_id')

def create_nested_structure(group):
    nested_dict = defaultdict(dict)
    
    for _, row in group.iterrows():
        dt_key = row['datetime']
        nested_dict[row['dev_id']][dt_key] = {
            'battery': row['battery'],
            'batteryDiff': row['batteryDiff'],
            'temperature': row['temperature'],
            'temperatureDiff': row['temperatureDiff'],
        }
    
    return dict(nested_dict)

result = {k: v for k, v in grouped_data.apply(create_nested_structure).items()}

for dev_id, data in result.items():
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    result[dev_id] = sorted_data

json_output = json.dumps(result, indent=2)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)