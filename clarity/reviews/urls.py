"""This is a urls file that runs different views through a specified path."""

from django.urls import path
from . import views

# Defining app name for reviews app.
app_name = 'reviews'

# Defining path to the reviews view.
urlpatterns = [
    path("", views.reviews, name="reviews"),
]