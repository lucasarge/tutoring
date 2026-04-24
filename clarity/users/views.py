from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView

# Create your views here.
class Login(LoginView):
    template_name = "users/login.html"

class Register(FormView):
    template_name = "users/register.html"