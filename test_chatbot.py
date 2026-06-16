import sys
from core.agent import CampusChatbot

bot = CampusChatbot()
response, tool, duration = bot.chat("Hello! What is your name?")
print(f"Tool: {tool} | Time: {duration}ms")

# Output safely on CP1252/Unicode consoles
encoding = sys.stdout.encoding or 'utf-8'
print("Response:", response.encode(encoding, errors='replace').decode(encoding))

