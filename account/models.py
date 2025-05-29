from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse
from .validators import validate_image_format
from PIL import Image
import os


class CustomUser(AbstractUser):
    followers = models.ManyToManyField("self", through='Contact', related_name="following_set", symmetrical=False)

    def get_absolute_url(self):
        return reverse('account:user_detail', args=[self.username])

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="profile_pictures/", validators=[validate_image_format], null=True, blank=True)
    photo_thumbnail = models.ImageField(upload_to="profile_thumbnails/", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            img.thumbnail((300, 300))
            name, ext = os.path.splitext(self.photo.name)
            ext = ext.lower()
            filename = os.path.basename(name + "_thumb" + ext)
            thumb_path = os.path.join(settings.MEDIA_ROOT, 'profile_thumbnails', filename)
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            img.save(thumb_path)
            self.photo_thumbnail = f"profile_thumbnails/{filename}"
            super().save(update_fields=['photo_thumbnail'])

    def __str__(self):
        return f"Profile of {self.user.username}"

class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_by_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_from', 'user_to')
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"