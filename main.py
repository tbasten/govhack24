import json
import requests

r = requests.get('https://services-ap1.arcgis.com/YQyt7djuXN7rQyg4/arcgis/rest/services/Mary_Cairncross_Scenic_Reserve_Dingtek_PIR_Counter/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson')
data = r.json()
features = data['features']
for feature in features:
    for property in feature['properties']:
        dev_id = feature['properties'].get('dev_id')
        datetime = feature['properties'].get('datetime')
        battery = feature['properties'].get('battery')
        people_count = feature['properties'].get('peopleCount')
        non_neg_people_count = feature['properties'].get('nonNegPeopleCount')
        object_id = feature['properties'].get('ObjectId')
        print(dev_id)