import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_friendly_gemini_response(user_input):
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        prompt = f"""
நீங்கள் ஒரு தமிழ் வாட்ச்மேன் அஸிஸ்டன்ட்.
யாராவது தற்போதைய இருப்பிடம், இடம், லொக்கேஷன், எங்கே, எங்க, இடம் போன்ற வார்த்தைகள் பயன்படுத்தினால் GPS_QUERY என பதிலளிக்கவும்.
யாராவது "அண்ணா நகர் செல்ல" அல்லது "சென்னை மெட்ரோக்கு வழி" போன்ற வாசகங்கள் கூறினால், DIRECTION_QUERY: <Destination> என பதிலளிக்கவும்.
மற்ற கேள்விகளுக்கு தமிழில் மரியாதையான பதில் அளிக்கவும்.

User Input: {user_input}
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini பிழை: {e}")
        return "மன்னிக்கவும், பதில் வழங்க முடியவில்லை."