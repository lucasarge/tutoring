"""This is a urls file that runs different views through a specified path."""

from django.urls import path
from . import views

# Defining app name for help app.
app_name = 'help'

# Defining path to the help view.
urlpatterns = [
    path("", views.help, name="help"),
]