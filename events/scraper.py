import requests
from bs4 import BeautifulSoup
from .models import Event

def scrape_events():
    url = 'https://www.timeout.com/sydney/things-to-do/free-things-to-do-in-sydney-today'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # ✅ Step 1: Get article blocks
    cards = soup.find_all("article", {"data-testid": "tile-zone-large-list_testID"})
    print(f"Found {len(cards)} cards")

    # ✅ Step 2: Loop through each card
    for card in cards:
        try:
            a_tag = card.find("a", href=True)
            if not a_tag:
                print("❌ Skipped: a_tag not found")
                continue

            title = a_tag.text.strip()
            link = "https://www.timeout.com" + a_tag["href"]
            date = "Today"
            location = "Sydney"

            # ✅ NEW: Get full event page content to fetch real description
            event_page = requests.get(link)
            event_soup = BeautifulSoup(event_page.text, 'html.parser')

            # More flexible tag targeting
            content_container = event_soup.find("div", attrs={"data-testid": "article-content"})
            if content_container:
                p_tag = content_container.find("p")
                description = p_tag.text.strip() if p_tag else "No description available"
            else:
                description = "No description available"

            obj, created = Event.objects.update_or_create(
                url=link,
                defaults={
                    "title": title,
                    "date": date,
                    "location": location,
                    "description": description
                }
            )
            print(f"✅ Saved: {obj.title} | Created: {created}")

        except Exception as e:
            print("❌ Error:", e)

    # ✅ Step 4: Final confirmation
    print("✅ Total saved:", Event.objects.count())
