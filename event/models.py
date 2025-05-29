from django.db import models
from django.conf import settings
from django.urls import reverse
from .validators import validate_image_format
from PIL import Image
import os

class Event(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event/images', validators=[validate_image_format], blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to='event/thumbnails', blank=True, null=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    date = models.DateTimeField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((300, 300))
            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename = os.path.basename(thumb_name + "_thumb" + thumb_extension)
            thumb_dir = os.path.join(settings.MEDIA_ROOT, 'event', 'thumbnails')
            os.makedirs(thumb_dir, exist_ok=True)
            thumb_path = os.path.join(thumb_dir, thumb_filename)
            img.save(thumb_path)
            self.image_thumbnail = f'event/thumbnails/{thumb_filename}'
            super().save(update_fields=['image_thumbnail'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event:event_details', args=[self.id])

class EventParticipant(models.Model):
    STATUS_CHOICES = (
        ('going', 'Going'),
        ('not_going', 'Not Going'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_participations'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user} - {self.event} ({self.status})"

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='event_comments'
        )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.event}"
