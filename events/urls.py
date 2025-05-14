from django.urls import path
from .views import run_scraper,event_list,save_ticket_interest,event_list_view

urlpatterns = [
    path('', event_list_view),
    path('scrape/', run_scraper),
    path('events/', event_list),
    path('save-interest/', save_ticket_interest),
]
