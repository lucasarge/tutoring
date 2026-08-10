"""Used to automate processes in this case for user creation."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

# Creates Profile model for user when user creates an account.
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)