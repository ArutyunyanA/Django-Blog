from django import template
from event.models import Event
from django.utils.timezone import now

register = template.Library()

@register.inclusion_tag('event/event_sidebar.html')
def upcoming_events(limit=5):
    events = Event.objects.filter(date__gte=now().date()).order_by('date', 'time')[:limit]
    return {'events': events}

@register.filter
def get_comment(comments, comment_id):
   return next((c for c in comments if c.id == int(comment_id)), None)