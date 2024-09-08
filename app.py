import flask
from flask import render_template, redirect, url_for
import pandas as pd


app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = False


def get_all_data_with_sensor(df, sensor_id):
    mask = df['dev_id'].astype(str).str.contains(sensor_id)
    
    return df[mask]


def create_nested_structure(location, location_data, parent=None):
    nested_structure = {}
    if parent:
        nested_structure[parent] = {}
    for asset_location, assets in location_data.items():
        nested_structure[asset_location] = {}
        for asset, sensors in assets.items():
            nested_structure[asset_location][asset] = {}
            for sensor_type, sensor_list in sensors.items():
                nested_structure[asset_location][asset][sensor_type] = {}
                for sensor_id in sensor_list:
                    nested_structure[asset_location][asset][sensor_type][sensor_id] = []
    return nested_structure

def get_nested_structure(df, sensor_map):
    nested_structure = create_nested_structure(None, sensor_map)
    
    for location, location_data in sensor_map.items():
        nested_structure[location] = create_nested_structure(location, location_data, location)
    
    for location, location_data in sensor_map.items():
        for asset_location, assets in location_data.items():
            for asset, sensors in assets.items():
                for sensor_type, sensor_list in sensors.items():
                    for sensor_id in sensor_list:
                        # Get data for this sensor
                        sensor_df = get_all_data_with_sensor(df, sensor_id)
                        
                        # Convert DataFrame to list of dictionaries
                        if sensor_type == 'temp':
                            sensor_data = sensor_df[['datetime', 'temperature', 'temperatureDiff']].to_dict('records')
                        
                        # Add to the nested structure
                        nested_structure[location][asset_location][asset][sensor_type][sensor_id] = sensor_data
    
    return dict(nested_structure)

sensor_map = {
    "Mary Cairncross Scenic Reserve": {
        "BBQ_East": {
            "BBQ_East_A001" : {
                "temp": [
                    "r718b140-06f8" 
                ]
            },
            "BBQ_East_A002" : {
                "temp": [
                    "r718b140-06fc" 
                ]
            },
            "BBQ_East_A003" : {
                "temp": [
                    "r718b140-06f9"   
                ]
            }
        },
        "BBQ_West": {
            "BBQ_West_A001": {
                "temp": [
                    "r718b140-06f7"
                ]
            },
            "BBQ_West_A002": {
                "temp": [
                    "r718b140-06fa"
                ]
            }
        }
    }
}

df = pd.read_csv('data/r718b140-06f7-BBQ Temp.csv')

data = get_nested_structure(df, sensor_map)

@app.route("/")
def home():
    return render_template("home.html", data = data)
@app.route("/test")
def admin():
    
    data={'id':1, 'name':'Josh'}
    return render_template("test.html", data = sensor_map)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)