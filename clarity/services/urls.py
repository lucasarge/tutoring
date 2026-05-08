from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path("invite/", views.invite, name="invite"),
    path("join/", views.join, name="join"),
    path("service/<int:pk>/", views.service, name="service"),
    path("invite-status/<int:pk>", views.invite_status, name="invite_status")
]
