from django.core.management.base import BaseCommand
from events.scraper import scrape_events

class Command(BaseCommand):
    help = 'Scrapes latest events from Timeout.com'

    def handle(self, *args, **kwargs):
        self.stdout.write("📅 Running event scraper...")
        scrape_events()
        self.stdout.write(self.style.SUCCESS('✅ Scraping complete.'))
