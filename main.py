import threading
import time
from listen import listen_tamil
from speak import speak_tamil
from gps import gps_listener, latest_gps_data
from navigation import navigation_tracker
from gemini import get_friendly_gemini_response

def process_audio(audio_queue, speaking_flag, last_speech_time):
    from direction import get_directions_to

    while True:
        if audio_queue and not speaking_flag[0]:
            user_input = audio_queue.pop(0)
            speaking_flag[0] = True
            response = get_friendly_gemini_response(user_input)

            if "GPS_QUERY" in response:
                speak_tamil(f"உங்கள் தற்போதைய இருப்பிடம்: {latest_gps_data[0]['address']}")

            elif "DIRECTION_QUERY:" in response:
                destination = response.split("DIRECTION_QUERY:")[1].strip()
                speak_tamil(f"{destination} செல்ல வழிமுறைகளை வழங்குகிறேன்...")
                get_directions_to(destination)

            else:
                speak_tamil(response)

            speaking_flag[0] = False

        if time.time() - last_speech_time[0] > 20:
            speak_tamil("தயவுசெய்து கூறுங்கள். உங்கள் உதவிக்கு நான் இருக்கிறேன்.")
            last_speech_time[0] = time.time()

        time.sleep(0.1)

if __name__ == '__main__':
    audio_queue = []
    speaking_flag = [False]
    last_speech_time = [time.time()]

    threading.Thread(target=listen_tamil, args=(audio_queue, last_speech_time), daemon=True).start()
    threading.Thread(target=process_audio, args=(audio_queue, speaking_flag, last_speech_time), daemon=True).start()
    threading.Thread(target=gps_listener, daemon=True).start()
    threading.Thread(target=navigation_tracker, daemon=True).start()

    while True:
        time.sleep(1)