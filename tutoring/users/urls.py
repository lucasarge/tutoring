from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import Login, Register, Logout

app_name = 'users'

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("logout", Logout.as_view(), name="logout")
    # path('profile', views.profile_view, name="profile"),
]