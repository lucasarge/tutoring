from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegisterForm, UpdateUserForm, ProfileImageForm
from django.contrib.auth import login

# Create your views here.
class Login(LoginView):
    template_name = "users/login.html"
    success_url = "/"

class Register(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = "/users/connect/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

def connect(request):
    return render(request, "users/connect.html")

@login_required    
def profile(request):

    user_form = UpdateUserForm(instance=request.user)
    image_form = ProfileImageForm(instance=request.user.profile)

    if request.method == "POST":

        if "info_submit" in request.POST:
            user_form = UpdateUserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect("/users/profile/")
        
        elif "image_submit" in request.POST:
            image_form = ProfileImageForm(
                request.POST, 
                request.FILES,
                instance=request.user.profile
            )
            if image_form.is_valid():
                image_form.save()
                return redirect("/users/profile/")


    return render(request, "users/profile.html", {
        "user_form": user_form,
        "image_form": image_form
    })
