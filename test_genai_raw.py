from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing direct Google GenAI SDK...")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash", # changed from 2.5 to 2.0 to match the app code model version just in case
        contents="Hello"
    )
    print("Success! Output:", response.text)
except Exception as e:
    print("Error:", e)
