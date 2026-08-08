"""This file defines database models and their fields."""

from django.db import models

# Model with question and answer field displaying the question on the admin dashboard.
class FAQ(models.Model):
    question = models.CharField()
    answer = models.TextField()

    def __str__(self):
        return self.question