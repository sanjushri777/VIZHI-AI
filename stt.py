import socket
import speech_recognition as sr
import os
import google.generativeai as genai
import pygame
import threading
import time
import json
import re
import googlemaps
from elevenlabs import ElevenLabs
from geopy.distance import geodesic

# API Configuration
genai.configure(api_key="AIzaSyDO7EKTL******")
client = ElevenLabs(api_key="sk_a809d497a8b6766bb8a*****")
gmaps = googlemaps.Client(key="AIzaSyDk0sp3JmQYPOluVLg*******")

latest_gps_data = [{"lat": None, "lng": None, "address": "Location not available"}]
route_steps = []
current_step_index = [0]

# GPS Listener
def gps_listener():
    HOST = '0.0.0.0'
    PORT = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print("Vizhi AI GPS listener ready...")

    conn, addr = server.accept()
    print(f"GPS Connected from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        gps_data = data.decode().strip()
        print("Location Data:", gps_data)
        try:
            gps_json = json.loads(gps_data)
            latest_gps_data[0]["address"] = gps_json.get("address", "Location not available")
            latest_gps_data[0]["lat"] = gps_json.get("lat")
            latest_gps_data[0]["lng"] = gps_json.get("lng")
        except Exception as e:
            print("JSON error:", e)

    conn.close()

# Listen English
def listen_english(audio_queue, last_speech_time):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio, language="en-US").strip()
                if text:
                    print(f"You said: {text}")
                    audio_queue.append(text)
                    last_speech_time[0] = time.time()
            except sr.UnknownValueError:
                print("Could not understand!")
            except sr.WaitTimeoutError:
                pass
            except sr.RequestError as e:
                print(f"Google Speech Recognition failed: {e}")
            except Exception as e:
                print(f"Error: {e}")

# Speak English
def speak_english(text):
    try:
        response = client.text_to_speech.convert(
            voice_id="gqFUMFHCD2nbbcYVtPGB",
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
        )
        audio_data = b"".join(response)
        filename = "response.mp3"
        with open(filename, "wb") as f:
            f.write(audio_data)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(filename)
    except Exception as e:
        print(f"ElevenLabs TTS Error: {e}")

# Directions + Step Tracker
def get_directions_to(destination_name):
    try:
        current_address = latest_gps_data[0]["address"]
        if "Location" in current_address:
            return ["Current location is unknown."]

        origin = gmaps.geocode(current_address)[0]["geometry"]["location"]
        destination = gmaps.geocode(destination_name)[0]["geometry"]["location"]

        directions = gmaps.directions(origin, destination, mode="walking", language="en")
        if not directions:
            return ["Directions not available."]

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
        print("Directions Error:", e)
        return ["An error occurred."]

# Navigation Tracker
def navigation_tracker():
    while True:
        if route_steps:
            lat = latest_gps_data[0]["lat"]
            lng = latest_gps_data[0]["lng"]

            if lat is None or lng is None:
                print("Waiting for GPS data...")
                time.sleep(5)
                continue

            current_pos = (lat, lng)
            target_step = route_steps[current_step_index[0]]
            target_pos = (target_step["lat"], target_step["lng"])
            distance = geodesic(current_pos, target_pos).meters
            print(f"Distance to next step: {distance:.2f} meters")

            if distance < 15:
                speak_english(target_step["text"])
                current_step_index[0] += 1
                if current_step_index[0] >= len(route_steps):
                    speak_english("You have reached your destination.")
                    route_steps.clear()
            elif distance > 40:
                speak_english("You are off track. Please turn around.")
        time.sleep(5)

# Gemini response
def get_friendly_gemini_response(user_input):
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        prompt = f"""
You're a helpful AI assistant designed specifically for blind or visually impaired users. 
Always respond using clear, friendly, and human-like English — no complicated words.

Here’s how to handle different types of requests:

1. If the user mentions "where am I", "my location", or "what’s around me" — Reply with: GPS_QUERY.
2. If the user says anything like "take me to", "navigate to", or "how do I reach [place]" — Reply with: DIRECTION_QUERY: <destination>.
3. If they’re asking anything else (e.g. general questions, chit-chat, time, weather, help, news) — Reply with a short, polite and easy-to-understand English response.
4. Always speak in a warm tone. Treat the user like a friend.
5. Never output HTML or code unless asked.
6. Keep responses under 20 seconds of speech.

Now here’s the user’s input:

User Input: {user_input}
"""
        response = model.generate_content(prompt)
        reply = response.text.strip()
        print("Gemini response:", reply)
        return reply
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Sorry, I couldn't provide an answer."

# Audio processor
def process_audio(audio_queue, speaking_flag, last_speech_time):
    while True:
        if audio_queue and not speaking_flag[0]:
            user_input = audio_queue.pop(0)
            speaking_flag[0] = True
            response = get_friendly_gemini_response(user_input)

            if "GPS_QUERY" in response:
                speak_english(f"Your current location is {latest_gps_data[0]['address']}")

            elif "DIRECTION_QUERY:" in response:
                destination = response.split("DIRECTION_QUERY:")[1].strip()
                speak_english(f"Providing directions to {destination}.")

                steps = get_directions_to(destination)
                for step in steps:
                    speak_english(step)
                    time.sleep(1)

            else:
                speak_english(response)

            speaking_flag[0] = False

        if time.time() - last_speech_time[0] > 20:
            speak_english("Please speak. I am here to help.")
            last_speech_time[0] = time.time()

        time.sleep(0.1)

# Init
audio_queue = []
speaking_flag = [False]
last_speech_time = [time.time()]

# Threads
threading.Thread(target=listen_english, args=(audio_queue, last_speech_time), daemon=True).start()
threading.Thread(target=process_audio, args=(audio_queue, speaking_flag, last_speech_time), daemon=True).start()
threading.Thread(target=gps_listener, daemon=True).start()
threading.Thread(target=navigation_tracker, daemon=True).start()

# Keep alive
while True:
    time.sleep(1)  