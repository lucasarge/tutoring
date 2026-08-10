"""This is a views file that holds functions or renders activated via url."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegisterForm, UpdateUserForm, ProfileImageForm
from django.contrib.auth import login

# This is the login page view which takes user to home if successful login with built in login form.
class Login(LoginView):
    template_name = "users/login.html"
    success_url = "/"

# This is the register page view which has a built in register form.
class Register(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm

    # If form is valid save user and login with users information.
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    # If user is caregiver redirect to invite page else if student redirect to join page.
    def get_success_url(self):
        user = self.request.user
        if user.user_type == "caregiver":
            return "/services/invite/"
        else:
            return "/services/join/"

# User needs to be logged in to access profile update page.
@login_required    
def profile(request):

    # Getting forms with instance as user to display previous answers.
    user_form = UpdateUserForm(instance=request.user)
    image_form = ProfileImageForm(instance=request.user.profile)

    # Checking if user is sending a response to the form.
    if request.method == "POST":
        if "info_submit" in request.POST:
            user_form = UpdateUserForm(request.POST, instance=request.user)

            # If form is valid save information and reload page.
            if user_form.is_valid():
                user_form.save()
                return redirect("/users/profile/")

        # If form submitted is image form connect to request.Files and save image.
        elif "image_submit" in request.POST:
            image_form = ProfileImageForm(
                request.POST, 
                request.FILES,
                instance=request.user.profile
            )

            # If form is valid save information and reload page.
            if image_form.is_valid():
                image_form.save()
                return redirect("/users/profile/")

    # Rendering 'profile.html' and parsing in context defined below.
    context = {"user_form": user_form, "image_form": image_form}
    return render(request, "users/profile.html", context)
