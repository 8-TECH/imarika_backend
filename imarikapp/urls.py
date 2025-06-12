# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerSubmissionView, PartnerSubmissionView, DonateSubmissionView

from .views import (
    ArticleViewSet,
    UpcomingEventsAPIView,
    PastEventsAPIView,
    ContactMessageViewSet,
    CreateEventWithImages,
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'contact', ContactMessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('events/upcoming/', UpcomingEventsAPIView.as_view(), name='upcoming-events'),
    path('events/past/', PastEventsAPIView.as_view(), name='past-events'),
    path('events/create-with-images/', CreateEventWithImages.as_view(), name='create-event-with-images'),
    path('events/<int:pk>/', CreateEventWithImages.as_view(), name='update-event-with-images'),
    path('submit/volunteer/', VolunteerSubmissionView.as_view(), name='submit-volunteer'),
    path('submit/partner/', PartnerSubmissionView.as_view(), name='submit-partner'),
    path('submit/donate/', DonateSubmissionView.as_view(), name='submit-donate'),
]