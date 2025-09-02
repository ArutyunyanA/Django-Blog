from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Profile, Contact

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Contact)
def notify_user_followed(sender, instance, created, **kwargs):
    if created:
        subject = f"New follower: {instance.user_from.username}"
        message = f"{instance.user_from.username} has followed on you!"
        send_mail(subject, message, 'noreply@yourblog.com', [instance.user_to.email])

@receiver(post_delete, sender=Contact)
def notify_user_infollowed(sender, instance, **kwargs):
    subject = f"{instance.user_from.username} unfollowed"
    message = f"{instance.user_from.username} not followed any more on you."
    send_mail(subject, f"You have been unfollowed by {instance.user_from.username}.", 'noreply@yourblog.com', [instance.user_to.email])
