from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth import login

# Create your views here.
class Login(LoginView):
    template_name = "users/login.html"
    success_url = "/"

class Register(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
def profile(request):
    return render(request, "users/profile.html")