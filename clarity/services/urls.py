"""This is a urls file that runs different views through a specified path."""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Defining app name for services app.
app_name = 'services'

# Defining path to the services view.
urlpatterns = [
    path("invite/", views.invite, name="invite"),
    path("join/", views.join, name="join"),
    path("invite-status/<int:pk>/", views.invite_status, name="invite_status"),
    path("<int:pk>/<str:page>/", views.service, name="service"),
    path("sessions/", views.all_sessions, name="all_sessions"),
    path("", views.all_services, name="all_services"),
    path("pdf/<int:resource_id>/", views.view_pdf, name="view_pdf"),
    path("session-link/<int:session_id>/", views.view_session_link, name="session_link"),
]

# This defines where the static files are located.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)