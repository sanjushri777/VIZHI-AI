import time
from geopy.distance import geodesic
from gps import latest_gps_data
from direction import route_steps, current_step_index
from speak import speak_tamil

def navigation_tracker():
    while True:
        if route_steps and latest_gps_data[0]["lat"] is not None:
            current_pos = (latest_gps_data[0]["lat"], latest_gps_data[0]["lng"])
            target_step = route_steps[current_step_index[0]]
            target_pos = (target_step["lat"], target_step["lng"])
            distance = geodesic(current_pos, target_pos).meters
            print(f"📏 Distance to next step: {distance:.2f} meters")

            if distance < 15:
                speak_tamil(target_step["text"])
                current_step_index[0] += 1
                if current_step_index[0] >= len(route_steps):
                    speak_tamil("நீங்கள் இலக்கை சென்றடைந்துவிட்டீர்கள்!")
                    route_steps.clear()
            elif distance > 40:
                speak_tamil("நீங்கள் தவறான பாதையில் உள்ளீர்கள். தயவுசெய்து திரும்பிச் செல்லவும்.")
        time.sleep(5)