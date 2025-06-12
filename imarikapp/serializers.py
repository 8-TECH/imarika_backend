from rest_framework import serializers
from .models import Article, Event, ContactMessage, EventImage, Volunteer, Partner, Donate

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['image']


class EventSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    images = EventImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_date', 'location', 'status', 'images']


class EventCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        event = Event.objects.create(**validated_data)
        for image in images:
            EventImage.objects.create(event=event, image=image)
        return event

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'



class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class DonateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donate
        fields = '__all__'
