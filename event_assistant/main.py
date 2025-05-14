import os
import requests
import openai
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
EVENT_API_URL = os.getenv("EVENT_API_URL")

# ✅ Step 1: Get user query
user_query = input("🧠 Ask me about events in Sydney: ")

# ✅ Step 2: Fetch all events from Django API
try:
    response = requests.get(EVENT_API_URL)
    events = response.json()
except Exception as e:
    print("❌ Failed to fetch events from Django:", e)
    exit()

# ✅ Step 3: Ask OpenAI to filter
system_prompt = (
    "You are a helpful assistant that recommends Sydney events to users "
    "based on their preferences. You will be given a list of events and a query."
    " Return the best 3 matches based on the user's interest."
)

# Format events into a simple list
formatted_events = "\n".join(
    [f"- {e['title']} | {e['date']} | {e['location']} | {e.get('description', '')[:100]}" for e in events]
)

# Ask GPT
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"My preferences: {user_query}"},
        {"role": "user", "content": f"Here are the events:\n{formatted_events}"}
    ],
    temperature=0.7
)

# ✅ Step 4: Show response
reply = completion['choices'][0]['message']['content']
print("\n🎯 Recommended Events:\n")
print(reply)
