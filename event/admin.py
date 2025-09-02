from django.contrib import admin
from .models import Event, EventParticipant

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'date', 'time', 'country', 'city']
    search_fields = ['title', 'country', 'city']

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status']
    list_filter = ['status']
