from django.db import models
from datetime import date

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    event_date = models.DateField()
    location = models.CharField(max_length=255)

    @property
    def status(self):
        return "Past" if self.event_date < date.today() else "Upcoming"

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')

    def __str__(self):
        return f"Image for {self.event.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    


class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Volunteer - {self.full_name}"

class Partner(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Partner - {self.full_name}"

class Donate(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mpesa_code = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donate - {self.full_name}"
