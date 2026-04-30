from django.urls import path
from .views import Login, Register
from . import views

app_name = 'users'

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("profile/", views.profile, name="profile")
]
