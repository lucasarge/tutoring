"""This file defines database models and their fields."""

from django.db import models
from users.models import CustomUser

# Review model with necessary fields displaying the reviews first name on the admin dashboard.
class Review(models.Model):

    # Constant that provides the different star rating options.
    STARS_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    stars = models.IntegerField(choices=STARS_CHOICES)
    message = models.TextField()
    used = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.user.first_name