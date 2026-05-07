from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("connect/", views.connect, name="connect"),
    path("<slug:slug>", views.service, name="service")
]
