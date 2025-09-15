from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

class Login(LoginView):
    template_name = "users/login.html"

class Register(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class Logout(LogoutView):
    next_page = "/"
    
# # Create your views here.
# def register_view(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             login(request, form.save())
#             return redirect("/")
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', { "form" : form })

# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect("/")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', { "form" : form })