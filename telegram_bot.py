import os
import requests
import openai
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def handle_message(update, context):
    user_text = update.message.text
    update.message.reply_text("🔍 Searching for events...")

    # Step 1: Get GPT summary
    gpt_reply = get_recommendations(user_text)
    update.message.reply_text("🤖 " + gpt_reply)

    # Step 2: Load events from your API
    try:
        events = requests.get(EVENT_API_URL).json()
    except Exception:
        update.message.reply_text("⚠️ Failed to load events.")
        return

    # Step 3: Send top 5 events as individual cards with buttons
    for event in events[:5]:
        title = event["title"]
        date = event["date"]
        location = event["location"]
        url = event["url"]
        description = event.get("description", "")[:150]

        message = f"📌 *{title}*\n📅 {date} | 📍 {location}\n📝 {description or 'No description.'}"

        keyboard = [[InlineKeyboardButton("🎫 Get Tickets", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# Load environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
EVENT_API_URL = os.getenv("EVENT_API_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Core logic: Get events from API + ask OpenAI
def get_recommendations(user_input):
    try:
        events = requests.get(EVENT_API_URL).json()
    except Exception as e:
        return "❌ Failed to fetch events."

    # Format events
    event_list = "\n".join(
        [f"- {e['title']} | {e['date']} | {e.get('description', '')[:100]}" for e in events]
    )

    # Ask LLM
    messages = [
        {"role": "system", "content": "You're an assistant helping users find events in Sydney."},
        {"role": "user", "content": f"User request: {user_input}"},
        {"role": "user", "content": f"Events:\n{event_list}"}
    ]

    try:
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )['choices'][0]['message']['content']
        return reply
    except Exception as e:
        return "⚠️ LLM Error: " + str(e)


# Start command
def start(update, context):
    update.message.reply_text("👋 Hi! Tell me what kind of event you're looking for in Sydney.")

# Launch bot
print("Loaded bot token:", TELEGRAM_BOT_TOKEN)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    print("🤖 Telegram bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
