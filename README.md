# Vizhi AI - Tamil Voice Assistant

Vizhi AI is a smart Tamil-speaking voice assistant built with Python that listens to voice commands, answers questions, provides current GPS location, and guides users with walking directions in Tamil it is built to embed in a neckband for providing emotional companion with help of Gemini.

---

## Features

- Recognizes Tamil speech using Google Speech Recognition
- Speaks responses in natural Tamil using ElevenLabs TTS
- Provides current GPS address (from external GPS feed)
- Gives walking directions using Google Maps API
- Understands context using Gemini AI
- Multi-threaded for real-time audio, GPS, and navigation handling

---

## How It Works

1. Listen: User speaks in Tamil.
2. Understand: Gemini AI classifies the query.
3. Respond:
   - If it's about location → GPS queried.
   - If it's a direction query → Google Maps directions provided.
   - Otherwise → Gemini generates a Tamil response.
4. Speak: ElevenLabs TTS speaks the response in Tamil.
5. Track Navigation: Tracks user location and gives turn-by-turn updates.

---

## Requirements

Install all Python packages with:

```bash
pip install -r requirements.txt
```

##Env 
```
1.Create a env file
2.add api key 
GEMINI_API_KEY=your_gemini_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
GMAPS_API_KEY=your_google_maps_api_key
```
## Run
```
  python main.py
```
