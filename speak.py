import os
import pygame
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

def speak_tamil(text):
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
        print(f"ElevenLabs TTS பிழை: {e}")