from datetime import date
from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Article, Event, EventImage, ContactMessage
from .serializers import (
    ArticleSerializer,
    EventSerializer,
    EventCreateSerializer,
    EventImageSerializer,
    ContactMessageSerializer,
)

# ARTICLES
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]  # Or IsAdminUser if updates should be admin-only

# CONTACT MESSAGES
class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-submitted_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]

# UPCOMING EVENTS
class UpcomingEventsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        upcoming_events = Event.objects.filter(event_date__gte=date.today()).order_by('event_date')
        serializer = EventSerializer(upcoming_events, many=True, context={'request': request})
        return Response(serializer.data)

# PAST EVENTS
class PastEventsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        past_events = Event.objects.filter(event_date__lt=date.today()).order_by('-event_date')
        serializer = EventSerializer(past_events, many=True, context={'request': request})
        return Response(serializer.data)

# CREATE / UPDATE / DELETE EVENT WITH IMAGES
class CreateEventWithImages(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            images = request.FILES.getlist('images')
            for img in images:
                EventImage.objects.create(event=event, image=img)
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            event = serializer.save()

            # Remove old images (optional depending on your UX design)
            event.images.all().delete()

            # Add new images if any
            images = request.FILES.getlist('images')
            for img in images:
                EventImage.objects.create(event=event, image=img)

            return Response(EventSerializer(event).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete related images explicitly if not handled automatically
        event.images.all().delete()
        event.delete()
        return Response({'detail': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics
from .models import Volunteer, Partner, Donate
from .serializers import VolunteerSerializer, PartnerSerializer, DonateSerializer
from rest_framework.permissions import AllowAny

class VolunteerSubmissionView(generics.CreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [AllowAny]

class PartnerSubmissionView(generics.CreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]

class DonateSubmissionView(generics.CreateAPIView):
    queryset = Donate.objects.all()
    serializer_class = DonateSerializer
    permission_classes = [AllowAny]
