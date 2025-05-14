from django.http import JsonResponse
from .scraper import scrape_events
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event,TicketInterest
from .serializers import EventSerializer
import json
from django.shortcuts import render
def run_scraper(request):
    scrape_events()
    return JsonResponse({"success": True, "message": "Events scraped successfully"})

@api_view(['GET'])
def event_list(request):
    events = Event.objects.all().order_by('-last_updated')
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)




def event_list_view(request):
    events = Event.objects.all().order_by('-last_updated')
    return render(request, 'events/list.html', {'events': events})

@csrf_exempt
def save_ticket_interest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        event_url = data.get("event_url")

        event = Event.objects.filter(url=event_url).first()
        if event and email:
            TicketInterest.objects.create(email=email, event=event)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Invalid event or email"}, status=400)

    return JsonResponse({"success": False, "error": "POST required"}, status=405)