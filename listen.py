import speech_recognition as sr
import time

def listen_tamil(audio_queue, last_speech_time):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("பேசுங்கள்...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio, language="ta-IN").strip()
                if text:
                    print(f"🗣 நீங்கள் கூறியது: {text}")
                    audio_queue.append(text)
                    last_speech_time[0] = time.time()
            except sr.UnknownValueError:
                print("புரியவில்லை!")
            except sr.WaitTimeoutError:
                pass
            except sr.RequestError as e:
                print(f"Google Speech Recognition தோல்வியடைந்தது: {e}")
            except Exception as e:
                print(f" பிழை: {e}")