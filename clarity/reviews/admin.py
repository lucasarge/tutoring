"""This is an admin file that is used to register the database models on the admin dashboard."""

from django.contrib import admin
from .models import Review

# Registering the database model Review to the admin dashboard.
admin.site.register(Review)