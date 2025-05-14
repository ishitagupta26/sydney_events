from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)

class TicketInterest(models.Model):
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.event.title}"
