import re
import googlemaps
import os
from dotenv import load_dotenv
from gps import latest_gps_data

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GMAPS_API_KEY"))

route_steps = []
current_step_index = [0]

def get_directions_to(destination_name):
    try:
        current_address = latest_gps_data[0]["address"]
        if "இருப்பிடம்" in current_address:
            return ["தற்போதைய இருப்பிடம் இல்லை."]

        origin = gmaps.geocode(current_address)[0]["geometry"]["location"]
        destination = gmaps.geocode(destination_name)[0]["geometry"]["location"]

        directions = gmaps.directions(origin, destination, mode="walking", language="ta")
        if not directions:
            return ["வழிமுறைகள் கிடைக்கவில்லை."]

        steps = directions[0]["legs"][0]["steps"]
        route_steps.clear()
        for step in steps:
            text = re.sub('<[^<]+?>', '', step["html_instructions"])
            lat = step["end_location"]["lat"]
            lng = step["end_location"]["lng"]
            route_steps.append({"text": text, "lat": lat, "lng": lng})
        current_step_index[0] = 0
        return [step["text"] for step in route_steps]
    except Exception as e:
        print("🚦 Directions Error:", e)
        return ["பிழை ஏற்பட்டது."]