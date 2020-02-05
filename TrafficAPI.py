import json
import requests

GOOGLE_API_KEY = ""

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_travel_time(event, get_traffic_time):
    if(get_traffic_time):
        parameters = {
            "origins": event.origin_address,
            "destinations": event.destination_address,
            "key": GOOGLE_API_KEY,
            "mode": "driving",
            "departure_time": "now",
        }
        print("in get traffic time")

    else:
        parameters = {
            "origins": event.origin_address,
            "destinations": event.destination_address,
            "key": GOOGLE_API_KEY,
        }
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?", params = parameters)
    jprint(response.json())
    if get_traffic_time:
        time = response.json()['rows'][0]['elements'][0]['duration_in_traffic']['value']
    else:
        time = response.json()['rows'][0]['elements'][0]['duration']['value']
    return time # in seconds