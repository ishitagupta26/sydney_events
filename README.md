-->Sydney Events Web App

This is a full-stack Django-based web application that automatically scrapes events in Sydney from Timeout.com and displays them beautifully. It includes email capture for "Get Tickets" actions and automatically updates events using a background task scheduler.
This project now includes a fully functional Telegram chatbot assistant using GPT-3.5 via OpenRouter, capable of recommending events based on user preferences.

--.Features

- Live event scraping** from Timeout Sydney using BeautifulSoup
-  Displays events with title, date, location, description, and ticket link
- Modern UI with Bootstrap 5 and responsive card layout
- Modal popup** for email capture before redirection
- Stores user email opt-ins in the database for analytics
- Automatic daily scraping** using Django management command + Task Scheduler
- GPT-powered event assistant** using OpenRouter (GPT-3.5)
- Integrated with Telegram bot to answer queries like:
  > “Any free events for students this weekend?”
-  Telegram replies include clickable Get Tickets buttons
- Intent matching and recommendation using OpenAI API via LangChain-style prompt
- Built using Python, Django, REST Framework, OpenAI, Telegram Bot API

-->Tech Stack
- Python 3.11
- Django 5.2
- Django REST Framework
- Bootstrap 5
- BeautifulSoup
- SQLite (default Django DB)

-->How to Run the Project
1. Clone or download this project.
2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows

-->Phase 2: GPT-Powered Telegram Assistant

The project includes an intelligent Telegram bot that:

- Accepts natural language queries (e.g., “free art events this weekend”)
- Uses GPT-3.5 (via OpenRouter) to interpret intent
- Fetches events from the Django backend
- Returns the top 3–5 relevant matches
- Includes clickable  Get Tickets buttons inside chat messages

To try it:

1. Start your Django server (`python manage.py runserver`)
2. Run the bot: `python telegram_bot.py`
3. Open Telegram and talk to your bot

Tech used: `python-telegram-bot`, OpenRouter GPT API, Django REST API
