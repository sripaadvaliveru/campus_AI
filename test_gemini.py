import os
from dotenv import load_dotenv

load_dotenv()

print("API Key:", os.getenv("GOOGLE_API_KEY"))
print("Length:", len(os.getenv("GOOGLE_API_KEY") or ""))

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", # changing 2.5 to 2.0 since it was 2.0 in the actual codebase (agent.py used gemini-2.0-flash-lite)
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    request_timeout=30
)

try:
    print(llm.invoke("Hello"))
except Exception as e:
    print("Exception:", e)
