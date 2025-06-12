from django.contrib import admin
from .models import Article, Event, ContactMessage, EventImage, Volunteer, Partner, Donate
from datetime import date

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'status_display')
    search_fields = ('title', 'location')
    list_filter = ('event_date',)
    inlines = [EventImageInline]

    def status_display(self, obj):
        return "Past" if obj.event_date < date.today() else "Upcoming"
    status_display.short_description = 'Status'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('submitted_at',)



@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'submitted_at']
    search_fields = ['full_name', 'email']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'submitted_at']
    search_fields = ['full_name', 'email']

@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'mpesa_code', 'submitted_at']
    search_fields = ['full_name', 'email', 'mpesa_code']
