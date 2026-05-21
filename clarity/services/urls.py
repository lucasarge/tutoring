from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path("invite/", views.invite, name="invite"),
    path("join/", views.join, name="join"),
    path("invite-status/<int:pk>/", views.invite_status, name="invite_status"),
    path("<int:pk>/<str:page>/", views.service, name="service"),
    path("sessions/", views.all_sessions, name="all_sessions")
]
