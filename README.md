# Vizhi AI — Real-Time AI Navigation and Emotional Assistant for the Visually Impaired

**Vizhi AI** is an intelligent, low-latency, neckband-based voice assistant designed to empower visually impaired individuals. It provides real-time navigation, context-aware AI conversations, and emotional assistance by integrating technologies such as Google Maps, ElevenLabs, Gemini AI, and Bluetooth-based Flutter communication.

Developed as a wearable neckband device, Vizhi AI enables instantaneous guidance, emotional companionship, and accessible mobility through ethical AI.

---

## Key Highlights

- Voice-controlled navigation using GPS and Google Maps  
- Real-time location tracking via Bluetooth (Flutter to Python backend)  
- Contextual and conversational AI powered by Google Gemini  
- Human-like audio feedback using ElevenLabs Text-to-Speech  
- Indoor-outdoor hybrid communication using Bluetooth and Sockets  
- Low-latency architecture optimized for wearable interaction  
- Wearable neckband form factor for hands-free experience  

---

## Demo

Coming soon.  
This section will include a demo video and screenshots showcasing how Vizhi AI works in real-life situations.

---

## Features

| Capability                  | Description                                                       |
|----------------------------|-------------------------------------------------------------------|
| Speech Recognition         | Accepts English input via microphone using natural language       |
| Turn-by-Turn Navigation    | Provides real-time voice alerts for directions                    |
| Google Maps Integration    | Live directions and geocoding support                             |
| Text-to-Speech             | Natural-sounding responses via ElevenLabs                         |
| GPS Location Streaming     | Real-time location transmission from Flutter to Python backend    |
| Conversational AI          | Context-aware and ethical dialogue through Gemini AI              |
| Accessibility-First Design | Specifically built for the visually impaired                     |
| Clear and Friendly Voice   | Warm and simple language with no technical jargon                 |

---

## System Architecture

### Flutter Mobile App
- Captures GPS coordinates
- Establishes Bluetooth connection automatically
- Sends real-time location to Python backend
- Fetches addresses from coordinates using reverse geocoding

### Python Backend
- Receives GPS data from the mobile app
- Processes speech input using voice recognition
- Sends queries to Gemini AI
- Uses Google Maps API for direction logic
- Tracks route and plays directional audio
- Converts AI responses into speech using ElevenLabs

---

## Technology Stack

| Technology        | Purpose                                             |
|-------------------|-----------------------------------------------------|
| Flutter            | Mobile interface and GPS/Bluetooth control         |
| Python             | Backend logic and AI processing                    |
| Gemini AI          | Conversational assistant engine                    |
| ElevenLabs         | Text-to-Speech audio synthesis                     |
| Google Maps API    | Navigation, directions, and geocoding              |
| Geopy              | Calculates distances between coordinates           |
| Socket             | Communication between app and backend              |
| SpeechRecognition  | Captures and interprets voice input                |
| Pygame             | Plays audio alerts and feedback                    |

---

## How to Run

### Prerequisites

- Python 3.8 or above  
- Flutter 2.10 or above  
- Android device with Bluetooth  
- API keys for:  
  - Google Maps  
  - ElevenLabs  
  - Gemini AI  

### Backend Setup (Python)

```bash
pip install -r requirements.txt
python main.py
cd flutter_app
flutter pub get
flutter run
```
##AI Prompt Design
```
Gemini AI is designed to:

Respond in a friendly, ethical, and helpful tone

Handle location and navigation queries like:

“Where am I?” → GPS_QUERY

“Navigate to Marina Beach” → DIRECTION_QUERY:<place>

Provide general assistance in warm and simple English

Avoid code or overly technical language in responses
```
##Privacy and Ethics
```
No user data is stored permanently

API key usage is secured and tokenized

All AI responses are monitored for fairness and clarity

Designed in accordance with the JobsForHer Ethical AI principles
```
##Credits
```
Developed with care by Sanjushri A,DURGADEVI P,SUBHASHINI B,ASWINI M 
Created for the Prime project 

Powered by:

Google Gemini AI

ElevenLabs Text-to-Speech

Google Maps API

Flutter

Python
```

