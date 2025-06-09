import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Directly set the API key here (not recommended for production)
genai.configure(api_key="AIzaSyBGWjPzqRL8KhQ135KOu_G7GkCf3Du3Ljg")

model = genai.GenerativeModel("models/gemini-1.5-pro")

def generate_linkedin_post(mood, length, language):
    prompt = (
        f"- Mood: {mood}\n"
        f"- Length: {length}\n"
        f"- Language: {language}\n"
        "The post should be engaging and professional."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except ResourceExhausted:
        return "API quota exceeded. Please try again later or check your quota."
    except Exception as e:
        return f"An error occurred: {str(e)}"
